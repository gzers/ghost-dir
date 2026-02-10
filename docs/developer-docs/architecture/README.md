# 架构文档

Ghost-Dir 架构设计文档索引（按当前代码实现维护）。

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 文档导航

## 架构来源说明

- 主架构文档（SSOT）：[`docs/architecture/README.md`](../../architecture/README.md)
- 本目录用于研发视角的工程化拆解与补充说明。

### `overview/` 架构概览

- [system-architecture.md](./overview/system-architecture.md): 系统分层、依赖规则、技术栈
- [core-modules.md](./overview/core-modules.md): 当前模块职责与边界
- [service-architecture-design.md](./overview/service-architecture-design.md): Service 层设计与协作方式
- [component-architecture.md](./overview/component-architecture.md): GUI 组件结构与约束

### `data-flow/` 数据流

- [data-flow-diagram.md](./data-flow/data-flow-diagram.md): 关键业务流程数据流

### `design-patterns/` 设计模式

- [patterns-used.md](./design-patterns/patterns-used.md): 项目中已落地的模式

### 配置系统

- [config-system.md](./config-system.md): 配置文件布局、初始化与恢复策略

## 当前真实分层（以 `src/` 为准）

```text
GUI (src/gui)
  -> Services (src/services)
  -> DAO + Drivers (src/dao, src/drivers)
  -> Models (src/models)
  -> Common (src/common)
```

依赖原则：
- 允许上层依赖下层。
- 禁止跨层反向依赖（如 `dao` 依赖 `gui`）。
- `common` 不依赖业务层；`models` 不依赖 `gui/services/dao/drivers`。

## 新开发者阅读顺序

1. [system-architecture.md](./overview/system-architecture.md)
2. [core-modules.md](./overview/core-modules.md)
3. [data-flow-diagram.md](./data-flow/data-flow-diagram.md)
4. [service-architecture-design.md](./overview/service-architecture-design.md)
5. [component-architecture.md](./overview/component-architecture.md)

## 文档维护规则

- 架构文档更新前，先核对真实目录：`src/common`、`src/models`、`src/dao`、`src/drivers`、`src/services`、`src/gui`。
- 历史术语 `core/data/utils` 不在主索引并列展示；仅可在迁移文档或归档文档说明。
