# 输出边界（Output Boundaries）

本文件定义 skill suite 的文件写入边界和角色边界。

## 编排器所有权（Orchestrator Ownership）

完整论文生成期间，`academic-paper-writer` 编排器拥有 `./docs/paper-drafts/` 下最终产物的写入权。

## 子 skill 所有权（Sub-Skill Ownership）

子 skill 返回结构化内容、报告、脚本、SVG 路径或建议输出路径。它们不得修改无关的项目源代码、配置、实验数据或既有产物。

## 独立使用（Independent Use）

当子 skill 被独立调用，且用户明确要求文件输出时，它可以在用户认可的路径中创建新输出文件。未经明确许可，不得覆盖已有数据。
