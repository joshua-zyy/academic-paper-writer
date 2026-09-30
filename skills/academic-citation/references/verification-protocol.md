# 两层引用核验

## 身份

真实打开原始出版页、官方 proceedings、arXiv 版本页或权威索引，核对标题、作者顺序、年份/版本、venue 及可用标识符。字段与来源匹配才标 identity_status VERIFIED；未核对 UNVERIFIED，冲突 CONFLICTING。记录来源与 checked_fields，不把字符串 VERIFIED 当证据。

DOI 可解析也需比对标题与作者；Crossref 无结果只说明该来源未查到，换出版方/其他权威来源，不据此判伪。预印本与正式版本年份不同先核对版本，不能一律视为错误。

本地 MD 是阅读载体，元数据仍核对；转换产物与原 PDF 是否匹配按实际内容/版本检查，时间戳只是线索。

## 主张支持

逐条核对正文陈述与原文片段：来源定位、必要摘录、条件与边界。supported / partial / contradicted / not_checked 使用共享引用映射契约。身份 VERIFIED 不自动生成 supported。

解释性分析核对相关文献是否真的讨论该解释、对象与条件；只表示相关不能改写成因果。reader 推断只作备注，不能作为原文引用。

全文不可读可按实际摘要给有限支持，明确 abstract_only；元数据/标题不能证明内容。未核验候选不进入确定性正式引用，用 REF_NEEDED 或建议补充。
