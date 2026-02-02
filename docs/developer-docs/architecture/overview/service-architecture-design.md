# Service 层架构设计文档 (Service Architecture Design)

## 1. 背景与目标
为了解决现有项目中 GUI 视图层（`LibraryView`, `ConnectedView`, `SettingView`）过度耦合业务逻辑的问题，本项目引入 **Service 层**。该层旨在实现业务逻辑、状态管理与 UI 表述的彻底解耦。

## 2. 核心架构模式
系统遵循 **View -> Service -> Data/Core** 的分层模式：
- **View**: 负责用户交互与数据渲染。
- **Service**: 负责业务逻辑编排、数据校验、异步任务管理及跨模块联动。
- **Data (Managers)**: 负责底层持久化存储与原子操作。

## 3. 服务职责划分

### 3.1 CategoryService
- **职责**: 管理分类（Category）的生命周期。
- **核心逻辑**: 重名检测、层级深度校验、分类删除时的模板清理/迁移逻辑。
- **UI 对接**: 为 `CategoryTreeWidget` 和 `CategorySelector` 提供格式化的展示数据。

### 3.2 TemplateService
- **职责**: 管理模板（Template）的业务逻辑。
- **核心逻辑**: 统一的搜索与过滤算法（结合分类 ID）、模板的 CRUD 编排、导入导出逻辑校验。
- **UI 对接**: 为 `TemplateTableWidget` 提供过滤后的数据源。

### 3.3 ConnectionService
- **职责**: 管理底层连接点（Link）的配置与运行状态。
- **核心逻辑**: 连接的创建/断开状态机、批量操作的原子性、后台扫描进程（Scan）与空间计算（SizeCalc）的生命周期管理。
- **UI 对接**: 为 `ConnectedView` 提供实时的链接状态看板。

### 3.4 ConfigService
- **职责**: 管理系统级配置（Theme, Paths, Behaviors）。
- **核心逻辑**: 配置变更的副作用执行（如自动刷新主题、更新全局变量）、`UserManager` 的上层封装。
- **UI 对接**: 为 `SettingView` 及其内部卡片提供配置状态。

## 4. 服务间通信与依赖
### 4.1 依赖关系 (Directional Dependency)
为了防止循环引用，必须遵循自上而下的依赖规范：
- `TemplateService` -> `CategoryService` (校验分类存在性)
- `ConnectionService` -> `TemplateService` (基于模板创建链接)
- 所有服务 -> `ConfigService` (获取基础参数)

### 4.2 通信方式 (Decoupled Communication)
- **方法调用**: 遵循单向依赖，可进行直接调用（Dependency Injection）。
- **SignalBus**: 跨模块的事件（如：应用根目录变更、分类被删除）统一通过 `src/common/signals/signal_bus.py` 进行广播。

## 5. 交互示例 (Data Flow)
以“手动删除一个带有模板的分类”为例：
1. **View**: 调用 `CategoryService.delete_category(id)`。
2. **CategoryService**: 
   - 检查该分类下是否有模板。
   - 若有，返回 `NEEDS_CONFIRM` 状态。
3. **View**: 展示确认弹窗。
4. **CategoryService**: 执行逻辑删除 -> 调用 `signal_bus.categories_changed.emit()`。
5. **TemplateService**: 监听到信号 -> 更新内部缓存 -> 重新应用过滤逻辑。

## 6. 后续维护建议
- 实施新的业务功能时，应优先在 Service 层定义接口并编写单元测试（Mock UI）。
- 禁止在 View 层直接实例化 Manager 类。
