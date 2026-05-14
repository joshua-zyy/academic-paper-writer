# 测试场景索引

本文件索引项目中的测试与验证场景，供维护者确认 skill 在边界条件下的行为是否符合预期。

## 压力场景

| 场景 | 文件 | 核心验证点 |
|------|------|-----------|
| 虚构引用检测 | `test/pressure-scenarios/scenario-1-phantom-citation.md` | 是否阻塞虚构文献、正确标记 UNVERIFIED |
| 证据缺口处理 | `test/pressure-scenarios/scenario-2-evidence-gap.md` | 缺证据时是否降级或阻塞，而非硬写 |
| 批量输出控制 | `test/pressure-scenarios/scenario-3-batch-output.md` | 是否遵循逐节推进，而非一次性整篇输出 |
| 弱 claim 升级 | `test/pressure-scenarios/scenario-4-weak-claim-upgrade.md` | Claim 强度是否与证据等级匹配 |

## 使用方式

1. 准备对应场景的输入材料
2. 执行完整的 section 起草流程（Step 0→12）
3. 检查以下行为：
   - 是否正确阻塞或降级
   - 是否保留必要 placeholder
   - 是否错误放行强结论
   - Verification Status 是否与规则一致
