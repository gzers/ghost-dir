# 开发文档

本目录包含面向开发者的技术文档、开发指南和贡献规范。

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 📂 目录结构

### [architecture/](./architecture/) - 架构设计

系统架构和设计文档:

- **[overview/](./architecture/overview/)** - 架构概览
  - [component-architecture.md](./architecture/overview/component-architecture.md) - 组件架构和关系
- **[design-patterns/](./architecture/design-patterns/)** - 设计模式
- **[data-flow/](./architecture/data-flow/)** - 数据流

### [development/](./development/) - 开发指南

开发过程中的规划、进度和报告:

- **[README.md](./development/README.md)** - 开发过程总览与治理规则
- **[setup/](./development/setup/)** - 开发环境搭建
- **[planning/](./development/planning/)** - 规划文档
  - [README.md](./development/planning/README.md) - 计划目录索引
  - [active/](./development/planning/active/) - 进行中的计划
  - [archived/](./development/planning/archived/) - 已归档的计划
- **[progress/](./development/progress/)** - 进度跟踪
  - [README.md](./development/progress/README.md) - 进度目录索引
  - [current/](./development/progress/current/) - 当前进度
  - [archived/](./development/progress/archived/) - 历史进度
- **[reports/](./development/reports/)** - 实施报告
  - [README.md](./development/reports/README.md) - 报告目录索引
  - [current/](./development/reports/current/) - 当前报告
  - [archived/](./development/reports/archived/) - 历史报告
- **[standardization-guide.md](./development/standardization-guide.md)** - 标准化开发规约 (路径/校验/分类)

### [testing/](./testing/) - 测试文档

测试相关的文档和报告:

- **[guides/](./testing/guides/)** - 测试指南
- **[test-plans/](./testing/test-plans/)** - 测试计划
- **[test-reports/](./testing/test-reports/)** - 测试报告

### [contributing/](./contributing/) - 贡献指南

如何为项目做贡献:

- **[guides/](./contributing/guides/)** - 贡献指南
- **[standards/](./contributing/standards/)** - 标准规范
- **[workflows/](./contributing/workflows/)** - 工作流程

---

## 📝 文档管理规范

### 状态标识
- `active`：当前维护中的主文档
- `archived`：历史文档，仅供追溯
- `obsolete`：已过期，待迁移或待删除

### 命名规范
- 使用小写+连字符(kebab-case)格式
- 避免使用版本号命名
- 使用描述性名称

### 文档生命周期
- **active/** - 进行中的文档
- **archived/** - 已完成的文档
- **current/** - 当前状态文档(定期更新)

说明：
- 目录名仅表示存放位置，不等同于有效状态。
- 文档是否可作为当前实施依据，以文首 `文档状态` 字段为准。

详细规范请参考 [标准化开发规约](./development/standardization-guide.md) 与计划文档：
- [文档专业化优化计划](./development/planning/active/docs-professionalization-plan.md)

---

**返回**: [文档主页](../README.md)
