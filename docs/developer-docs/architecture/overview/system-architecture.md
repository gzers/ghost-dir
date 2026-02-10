# Ghost-Dir 系统架构

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 概述

Ghost-Dir 采用严格的**五层金字塔架构**,确保代码清晰、可维护、易测试。所有依赖关系单向向下,Models 和 Common 作为最底层基础。

## 五层金字塔架构图

```
               [GUI 表现层]
                 │    │
      ┌──────────┘    │
      │               ↓
      │          [Services 业务层] ────────────┐
      │           │            │               │
      │           ↓            ↓               │
      │      [Drivers 驱动层] [DAO 数据层]     │
      │           │            │               │
      └─────┬─────┴──────┬─────┴───────┘       │
            │            │                     │
            ↓            ↓                     │
        [Models 数据定义] [Common 基础层] <──────┘
            │            │
            └─────┬──────┘
                  ↓
         [Python 标准库]
```

## 架构分层

### Level 1: GUI 表现层

**模块**: `src/gui/`

**职责**:
- 用户交互处理
- 数据展示
- 视图状态管理
- 样式和主题管理
- 国际化支持

**依赖**: Services, Models, Common

**主要组件**:
- `app.py` - 应用主类,管理应用生命周期
- `windows/` - 主窗口和子窗口
- `views/` - 功能视图页面 (links, wizard, library, settings, help)
- `dialogs/` - 对话框组件
- `components/` - 可复用UI组件
- `styles/` - 样式系统和主题
- `i18n/` - 国际化和本地化

### Level 2: Services 业务层

**模块**: `src/services/`

**职责**:
- 业务逻辑编排
- 流程控制
- 业务规则实现
- 协调 DAO 和 Drivers

**依赖**: DAO, Drivers, Models, Common

**主要组件**:
- `template_svc.py` - 模板业务逻辑
- `link_svc.py` - 链接业务逻辑
- `category_svc.py` - 分类业务逻辑
- `scan_svc.py` - 扫描逻辑编排 (规划中)
- `wizard_svc.py` - 向导逻辑 (规划中)

### Level 3: DAO 数据层 & Drivers 驱动层

#### DAO 数据访问层

**模块**: `src/dao/`

**职责**:
- 数据持久化 (JSON)
- CRUD 操作
- 数据查询

**依赖**: Models, Common

**主要组件**:
- `template_dao.py` - 模板数据持久化
- `link_dao.py` - 链接数据持久化
- `category_dao.py` - 分类数据持久化

#### Drivers 驱动层

**模块**: `src/drivers/`

**职责**:
- 系统底层操作
- Windows API 封装
- 文件系统操作
- 事务管理

**依赖**: Models (可选), Common

**主要组件**:
- `windows.py` - Junction 操作, UAC 检查
- `fs.py` - 文件系统工具
- `transaction.py` - 事务管理引擎
- `process.py` - 进程检测

### Level 4: Models 数据定义层

**模块**: `src/models/`

**职责**:
- 数据结构定义
- 基础验证逻辑
- 实体模型

**依赖**: Common (仅限工具函数和常量)

**严禁依赖**: GUI, Services, DAO, Drivers

**主要组件**:
- `template.py` - Template 实体
- `link.py` - UserLink 实体
- `category.py` - CategoryNode 实体

### Level 5: Common 基础层

**模块**: `src/common/`

**职责**:
- 全局配置管理
- 自定义异常定义
- 全局信号定义
- 纯工具函数

**依赖**: 无 (只能使用 Python 标准库)

**主要组件**:
- `config.py` - 全局配置和常量
- `signals.py` - 全局信号定义
- `exceptions.py` - 自定义异常
- `validators/` - 路径与名称校验器

## 依赖规则

### 允许的依赖 (箭头向下)

| 层级 | 可以 import |
|------|------------|
| GUI | Services, Models, Common |
| Services | DAO, Drivers, Models, Common |
| DAO | Models, Common |
| Drivers | Models (可选), Common |
| Models | Common (仅限工具和常量) |
| Common | 无 (只能用标准库) |

### 绝对禁止的依赖

**Models 层的铁律**:
- ❌ 不能 import GUI
- ❌ 不能 import Services
- ❌ 不能 import DAO
- ❌ 不能 import Drivers
- ✅ 只能 import Common

**Common 层的铁律**:
- ❌ 不能 import 任何项目代码
- ✅ 只能使用 Python 标准库

**其他层**:
- ❌ 任何层不能反向依赖上层
- ❌ 不能跨层依赖 (如 GUI 直接依赖 DAO)

## 架构设计原则

### 1. 依赖单向向下

- 上层依赖下层,绝不反向
- 防止循环依赖
- 保持架构清晰

### 2. Models 和 Common 是基础

- 所有层都可以使用 Models (数据定义)
- 所有层都可以使用 Common (工具和配置)
- 但 Models 和 Common 不依赖任何层

### 3. 职责单一

- 每层只做自己的事,不越界
- GUI 只负责展示
- Services 只负责业务逻辑
- DAO 只负责数据持久化
- Drivers 只负责系统操作
- Models 只负责数据定义
- Common 只负责基础设施

### 4. 金字塔结构

- 越底层越稳定
- 越上层越易变
- 底层变化影响大,需谨慎
- 上层变化影响小,可灵活

## 技术栈

### 核心框架
- **PySide6** - Qt for Python, GUI 框架
- **Python 3.8+** - 编程语言

### UI 组件库
- **qfluentwidgets** - Fluent Design 风格组件库

### 数据存储
- **JSON** - 配置和数据持久化
- **文件系统** - 模板和用户数据存储

### 开发工具
- **Git** - 版本控制
- **pytest** - 单元测试 (规划中)

## 关键设计决策

### 1. 为什么采用五层金字塔架构?

- **可维护性**: 清晰的层次便于理解和维护
- **可测试性**: 每层可独立测试
- **可扩展性**: 新功能可在合适的层添加
- **防止混乱**: 严格的依赖规则防止循环依赖

### 2. 为什么 Models 和 Common 在最底层?

- **共享性**: 所有层都需要使用数据定义和基础工具
- **稳定性**: 底层变化影响大,需要最稳定
- **纯净性**: 不依赖任何业务逻辑,保持纯净

### 3. 为什么使用 JSON 而非数据库?

- **轻量级**: 无需额外的数据库依赖
- **可读性**: 配置文件易于查看和编辑
- **便携性**: 数据文件可直接复制迁移
- **适用性**: 数据量小, JSON 足够满足需求

### 4. 为什么使用信号槽机制?

- **解耦**: 组件间无需直接引用
- **灵活**: 一对多通信简单实现
- **线程安全**: Qt 自动处理跨线程信号

## 性能考虑

### 1. 异步操作

- 文件扫描使用 `QThread` 避免 UI 冻结
- 大量数据处理使用工作线程
- 进度反馈通过信号实时更新

### 2. 资源管理

- 延迟加载: 按需加载资源和组件
- 缓存机制: 缓存常用数据和计算结果
- 及时释放: 不再使用的资源及时清理

### 3. UI 优化

- 虚拟滚动: 大列表使用虚拟化技术
- 防抖节流: 频繁操作使用防抖/节流
- 批量更新: 批量 DOM 更新减少重绘

## 安全考虑

### 1. 文件操作安全

- 路径验证: 检查路径合法性 (黑名单机制)
- 权限检查: 验证操作权限 (UAC)
- 事务保护: 关键操作使用事务引擎

### 2. 数据验证

- 输入验证: 验证用户输入
- 类型检查: 使用类型注解
- 边界检查: 检查数组越界等

### 3. 错误处理

- 异常捕获: 捕获并处理异常
- 错误日志: 记录错误信息
- 用户提示: 友好的错误提示

## 扩展性设计

### 1. 插件机制 (规划中)

- 支持第三方插件
- 插件独立加载和卸载
- 插件 API 标准化

### 2. 主题系统

- 支持自定义主题
- 动态切换主题
- 主题配置外部化

### 3. 国际化

- 多语言支持
- 语言包独立管理
- 运行时切换语言

## 相关文档

- [组件架构文档](./component-architecture.md) - GUI 组件化设计
- [核心模块文档](./core-modules.md) - 各模块详细说明
- [数据流文档](../data-flow/data-flow-diagram.md) - 数据流转说明
- [设计模式文档](../design-patterns/patterns-used.md) - 设计模式应用
- [架构设计文档](../../../architecture/README.md) - 完整架构设计
