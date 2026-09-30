# 准备与首轮并行探查

## 1. 接收与集中确认

先读用户已有材料、请求与已确认状态。识别全文、章节、段落或专项范围；不先问能从材料获得的事实。

全文任务集中确认必要缺项：材料位置与研究想法、写作语言、auto（默认）或 step-by-step。venue 可未定；引用数量可不填，若提供也仅建议。已明确自动模式无需再次询问。

局部请求只确认影响当前结果的歧义。单段不要求仓库、venue 或全文证据包。

## 2. 启动建库建议

主动建议将本地 PDF 用 MinerU 转成 MD 建库；分别说明待引用参考库与目标 venue 风格库。已建库直接复用，新增论文按需增量转换。API 会上传 PDF，未公开或敏感资料需确认；token 只放环境变量。

示例（将 `<skill_dir>` 换成当前 academic-citation 所在绝对路径，不猜安装目录）：

```powershell
$env:MINERU_API_TOKEN = "<token>"
python "<skill_dir>/scripts/convert-pdfs-to-md.py" "<pdf_dir>" "<md_dir>" --type ref
# 风格库使用 --type style
```

转换后优先使用 `_index_ref.json` / `_index_style.json` 检索；没有索引也可按文件名和可读内容定向查找。不是所有 PDF 都必须先转，元数据核验无需全文；所需内容不可读只阻塞依赖它的判断。

## 3. 首轮任务划分

主 agent 先简短盘点材料位置，再并行派发不重叠任务：

- 方法：probe-agent，代码运算/模块/输入输出，以及作者已给出的动机。
- 实验：academic-experiments，已有配置、协议、表格、结果及来源，只读默认。
- 文献：academic-citation，按研究问题本地优先，再补必要公开文献；身份与支持分开。
- venue 已知且要求影响内容时：academic-venue-research；官方要求与风格观察分开。没 venue 不暂停。

没有代码或结果时不造空任务；转而读取笔记、想法、草稿。同一来源指定负责者，避免多代理重复读库。子代理工具不可用时主 agent 承担同样取证职责，说明降级，不伪造派发记录。

## 4. 派发包

```yaml
task_id: P001
role: probe | experiments | citation | venue
question: "需要回答的具体问题"
read_scope: ["材料路径或公开来源范围"]
known_evidence_ids: [E001]
relevant_sections: [method]
authorization: read_only
output: "事实+具体定位+冲突+缺口；遵循共享证据或引用契约"
prohibitions: ["不写正文", "不改源文件", "不擅自执行", "不扩展研究范围"]
completion_condition: "问题已回答，或明确说明未能回答及所缺材料"
```

允许读取相关调用链，不硬限制只有直接子目录；避开无关缓存和私密材料。子代理失败保留已有效结果，诊断具体原因后定向补查，不重复整轮任务。

## 5. 主 agent 合并

合并 evidence_inventory、引用身份记录、citation_to_claim_map，去重并保留来源。作者意图、假设、已报告结果、已核对事实分别标注；摘要可读不能宣称全文已读。

识别已有内容足以写成正文的章节与需要框架的部分。对冲突优先核对实际运行配置和产物，仍不明则集中向作者询问；不判定实验是否优秀，不默认执行评估 checkpoint。

## 6. 执行与补证决策

重算/统计仅在预先限定授权内；新实验、重训、变更协议单独批准。高成本补证先说明缺什么、影响、预计代价与可交付替代，让作者选继续或交现有稿。其余独立工作继续。

主线确认后，证据包可跨章节复用。定向补查必须给出具体缺口和已有 evidence_ids，不能每节重跑本阶段。
