# Ghost-Dir 架构文档

## 项目架构概览

Ghost-Dir 采用**五层金字塔架构**,从底层到顶层依次为:

```
┌─────────────────────────────────┐
│         GUI Layer (Level 1)      │  表现层
├─────────────────────────────────┤
│      Services Layer (Level 2)    │  业务逻辑层
├─────────────────────────────────┤
│   DAO/Drivers Layer (Level 3)    │  数据访问/系统驱动层
├─────────────────────────────────┤
│      Models Layer (Level 4)      │  数据模型层
├─────────────────────────────────┤
│      Common Layer (Level 5)      │  全局基础层
└─────────────────────────────────┘
```

## 目录结构

```
src/
├── gui/             # Level 1: 表现层
│   ├── components/  # 可复用组件
│   ├── dialogs/     # 对话框
│   ├── views/       # 视图页面
│   ├── windows/     # 主窗口
│   └── i18n/        # 国际化
├── services/        # Level 2: 业务逻辑层
│   ├── template_service.py
│   ├── link_service.py
│   └── category_service.py
├── dao/             # Level 3: 数据访问层
│   ├── template_dao.py
│   ├── link_dao.py
│   └── category_dao.py
├── drivers/         # Level 3: 系统驱动层
│   ├── fs.py        # 文件系统操作
│   ├── transaction.py
│   └── windows.py
├── models/          # Level 4: 数据模型层
│   ├── template.py
│   ├── link.py
│   └── category.py
└── common/          # Level 5: 全局基础层
    ├── config.py
    ├── signals.py
    ├── service_bus.py  # 全局 Service 访问点
    └── managers.py     # 临时兼容层
```

## 层级职责

### Level 1: GUI Layer (表现层)
- **职责**: 用户界面展示和交互
- **依赖**: Services Layer
- **特点**: 不直接访问 DAO 或 Models

### Level 2: Services Layer (业务逻辑层)
- **职责**: 封装业务逻辑,协调 DAO 和 Models
- **依赖**: DAO Layer, Models Layer
- **特点**: 无状态,可复用

### Level 3: DAO/Drivers Layer (数据访问/系统驱动层)
- **DAO**: 数据持久化操作 (JSON 文件读写)
- **Drivers**: 系统级操作 (文件系统、Windows API)
- **依赖**: Models Layer
- **特点**: 与具体实现相关

### Level 4: Models Layer (数据模型层)
- **职责**: 定义数据结构
- **依赖**: 无 (纯数据类)
- **特点**: 使用 `@dataclass`,包含序列化/反序列化方法

### Level 5: Common Layer (全局基础层)
- **职责**: 全局配置、工具函数、信号总线
- **依赖**: 无
- **特点**: 被所有层使用

## 数据流

### 读取数据流
```
GUI → Service → DAO → JSON File
                ↓
              Models
```

### 写入数据流
```
GUI → Service → DAO → JSON File
        ↓
      Models
```

## 兼容层 (临时)

为了保持向后兼容,当前实现了两个临时模块:

### `common/service_bus.py`
全局 Service 访问点,提供单例访问:
```python
from src.common.service_bus import service_bus

# 访问 Service
templates = service_bus.template_service.get_all_templates()

# 访问 Manager (兼容旧代码)
templates = service_bus.template_manager.get_all_templates()
```

### `common/managers.py`
Manager 包装器,内部调用 Service:
```python
class TemplateManager:
    def __init__(self):
        self._service = TemplateService(TemplateDAO())
    
    def get_all_templates(self):
        return self._service.get_all_templates()
```

**注意**: 这些兼容层是临时方案,后续应逐步移除,GUI 层直接使用 Service。

## 依赖注入

Services 通过构造函数注入 DAO:
```python
class TemplateService:
    def __init__(self, dao: TemplateDAO):
        self.dao = dao
```

这样设计的好处:
- 便于单元测试 (可以注入 Mock DAO)
- 降低耦合度
- 提高可维护性

## 配置管理

配置文件存储在 `.ghost-dir/` 目录:
- `config.json`: 应用配置
- `templates.json`: 模板数据
- `categories.json`: 分类数据
- `links.json`: 用户链接数据

使用 `get_config_path()` 函数获取配置文件路径:
```python
from src.common.config import get_config_path

config_file = get_config_path('templates.json')
```

## 最佳实践

1. **单向依赖**: 上层可以依赖下层,下层不能依赖上层
2. **接口隔离**: Service 提供清晰的接口,隐藏实现细节
3. **数据封装**: 使用 Models 传递数据,不直接传递字典
4. **错误处理**: 在 Service 层统一处理错误
5. **日志记录**: 在关键操作点记录日志

## 后续优化方向

1. **移除兼容层**: 逐步移除 Manager 和 service_bus
2. **依赖注入容器**: 使用 DI 容器管理依赖
3. **事件驱动**: 使用事件总线解耦模块
4. **单元测试**: 为每层添加单元测试
5. **文档完善**: 添加 API 文档和使用示例
