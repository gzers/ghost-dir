# 架构文档

Ghost-Dir 架构设计文档索引。

## 📂 文档导航

### [overview/](./overview/) - 架构概览

系统整体架构和模块说明:

- **[system-architecture.md](./overview/system-architecture.md)** - 系统整体架构
  - 架构分层(表现层/业务层/核心层/基础层)
  - 技术栈说明
  - 架构设计原则
  - 模块依赖关系
  
- **[core-modules.md](./overview/core-modules.md)** - 核心模块详解
  - Common模块(配置、信号、资源)
  - Core模块(扫描、链接、安全、事务)
  - Data模块(模型、管理器)
  - Utils模块(工具函数)
  
- **[component-architecture.md](./overview/component-architecture.md)** - GUI组件架构
  - 组件化设计原则
  - 组件文件结构
  - 组件依赖关系
  - 最佳实践

### [data-flow/](./data-flow/) - 数据流

数据在系统中的流转:

- **[data-flow-diagram.md](./data-flow/data-flow-diagram.md)** - 数据流图
  - 应用启动流程
  - 智能扫描流程
  - 导入模板流程
  - 分类管理流程
  - 数据持久化
  - 数据验证

### [design-patterns/](./design-patterns/) - 设计模式

项目中使用的设计模式:

- **[patterns-used.md](./design-patterns/patterns-used.md)** - 设计模式应用
  - 单例模式(全局信号)
  - 管理器模式(数据管理)
  - 观察者模式(信号槽)
  - 策略模式(冲突处理)
  - 模板方法模式(基础页面)
  - 组合模式(分类树)
  - 其他模式

### 配置系统

配置文件系统架构设计:

- **[config-system.md](./config-system.md)** - 配置系统架构规范 ✨
  - 官方与用户配置分离
  - 配置文件结构(开发/打包环境)
  - 配置恢复功能设计
  - UI交互流程
  - 代码实现规范

---

## 🚀 快速开始

### 新开发者入门

1. **了解整体架构**: 阅读 [系统架构概览](./overview/system-architecture.md)
2. **理解模块职责**: 阅读 [核心模块](./overview/core-modules.md)
3. **学习数据流**: 阅读 [数据流图](./data-flow/data-flow-diagram.md)
4. **掌握设计模式**: 阅读 [使用的设计模式](./design-patterns/patterns-used.md)
5. **查看组件设计**: 阅读 [组件架构](./overview/component-architecture.md)

### 开发新功能

1. 确定功能所属层次(表现层/业务层/核心层)
2. 选择合适的模块(gui/data/core/common/utils)
3. 遵循现有的设计模式
4. 使用信号槽解耦组件
5. 更新相关文档

---

## 📋 架构原则

### 1. 分层架构

- 表现层 → 业务层 → 核心层 → 基础层
- 单向依赖,上层依赖下层
- 层间通过清晰的接口通信

### 2. 模块化

- 高内聚,低耦合
- 每个模块职责单一
- 模块可独立测试和替换

### 3. 组件化

- UI组件独立文件
- 组件可复用
- 通过组合构建复杂功能

### 4. 信号驱动

- 使用Qt信号槽解耦
- 异步处理长时间操作
- 响应式UI更新

---

## 🔍 架构图

### 系统分层

```
┌─────────────────────────────────────┐
│     Presentation Layer (GUI)        │
│  Views | Dialogs | Components       │
├─────────────────────────────────────┤
│   Business Logic Layer (Data)       │
│  CategoryMgr | TemplateMgr | Model  │
├─────────────────────────────────────┤
│      Core Layer (Core)              │
│  Scanner | LinkOpt | Safety | Tx    │
├─────────────────────────────────────┤
│  Infrastructure Layer (Common)      │
│  Config | Signals | Resources       │
└─────────────────────────────────────┘
```

### 模块关系

```
gui ──┬──> data ──> core ──> common
      │                └──> utils
      └──> common
```

---

## 📖 相关文档

- [开发文档主页](../../README.md)
- [开发指南](../../development/) - 开发流程和规范
- [测试文档](../../testing/) - 测试指南和报告
- [贡献指南](../../contributing/) - 如何贡献代码

---

**最后更新**: 2026-01-28
