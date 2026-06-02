# Venue Research Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 来源混淆 | 将已录用论文观察当作 venue 规范要求 | 严格区分一级证据（官方 guidelines）和二级证据（论文观察） |
| 缓存欺骗 | 将 webfetch 缓存页面当作最新 CFP | 必须标注 fetch 时间戳 |
| 来源不透明 | 信息不标注来源类型 | 所有信息标注来源（webfetch / agent_knowledge / Unknown） |
| 低层级包装 | 将非官方博客或第三方总结写成 author guidelines | 必须是一级官方来源 |
