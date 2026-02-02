# Service 层架构设计文档 (Service Architecture Design)

## 1. 背景与目标
为了解决现有项目中 GUI 视图层（`LibraryView`, `ConnectedView`, `SettingView`）过度耦合业务逻辑的问题，本项目引入 **Service 层**。该层旨在实现业务逻辑、状态管理与 UI 表述的彻底解耦。

## 2. 核心架构模式
系统遵循 **View -> Service -> Data/Core** 的分层模式：
- **View**: 负责用户交互与数据渲染，仅持有对 Service 的引用。
- **Service**: 负责业务逻辑编排、数据校验、异步任务管理及跨模块联动。
- **Data (Managers)**: 负责底层持久化存储与原子操作，不直接与 View 通信。

## 3. 服务职责划分

### 3.1 CategoryService
- **职责**: 管理分类（Category）的生命周期与层级逻辑。
- **核心逻辑**: 重名检测、层级深度校验、分类删除时的级联模板清理或静默迁移逻辑。
- **UI 对接**: 为 `CategoryTreeWidget` 和 `CategorySelector` 提供格式化的数据流或 ViewModel。

### 3.2 TemplateService
- **职责**: 管理模板（Template）的业务逻辑与聚合操作。
- **核心逻辑**: 统一的搜索与多维过滤算法、模板 CRUD 的事务性编排、导入导出时的格式合法性校验。
- **UI 对接**: 为 `TemplateTableWidget` 提供经过过滤和排序的逻辑数据源。

### 3.3 ConnectionService
- **职责**: 管理底层连接点（Link）的配置与运行状态。
- **核心逻辑**: 维护连接的全生命周期状态机、批量操作的原子性、后台扫描进程（Scan）与空间计算（SizeCalc）的任务调度。
- **UI 对接**: 为 `ConnectedView` 提供实时的链接状态 Kanban 或状态流。

### 3.4 ConfigService
- **职责**: 管理系统级配置与全局状态。
- **核心逻辑**: 配置变更的副作用执行（如动态切换主题、全局存储路径更新）、对底层 `UserManager` 的业务级封装。
- **UI 对接**: 为 `SettingView` 及其内部卡片提供配置绑定。

## 4. 服务间通信与依赖
### 4.1 依赖关系 (Directional Dependency)
为了防止循环引用，必须遵循自上而下的依赖规范：
- `TemplateService` -> `CategoryService` (用于删除分类前的归属校验)
- `ConnectionService` -> `TemplateService` (用于基于特定模板实例创建链接)
- **所有服务** -> `ConfigService` (用于获取基础路径或全局参数)

### 4.2 通信方式 (Decoupled Communication)
- **方法调用**: 遵循单向依赖原则，上层对下层进行直接方法调用（Dependency Injection）。
- **SignalBus**: 跨模块的事件（如：应用根目录变更、分类被删除后的副作用）统一通过 `src/common/signals/signal_bus.py` 进行广播。

## 5. 交互示例 (Data Flow)
以“手动删除一个带有模板的分类”为例：
1. **View**: 调用 `CategoryService.delete_category(id)` 发起删除动作。
2. **CategoryService**: 
   - 内部检查该分类下是否存在关联模板。
   - 若存在依赖，返回 `REQUIRED_CONFIRM` 状态及其上下文信息。
3. **View**: 根据返回状态展示确认弹窗。
4. **CategoryService**: 用户确认后，执行原子删除逻辑 -> 触发 `signal_bus.categories_changed.emit()`。
5. **TemplateService**: 监听到信号 -> 更新内部缓存索引 -> 重新触发当前 UI 的过滤逻辑。

## 6. 后续维护建议
- **逻辑下沉**: 实施新业务功能时，应优先在 Service 层定义接口并编写单元测试（Mock UI）。
- **禁止旁路**: 严禁在 View 层直接实例化或调用 Manager 类，必须通过对应的 Service 进行收口。
- **状态一致性**: 涉及多个 Manager 的操作必须在 Service 中封装为原子事务，确保数据一致性。

## 7. 高级工程化补充 (Planned Enhancements)

### 7.1 I18nService (运行时动态语言切换)
- **发现**: 现有的 `t()` 函数主要在初始化时生效，且翻译逻辑零散。
- **方案**: 引入 `I18nService` 中控。当语言变更时，通过 Service 触发全局信号，由各基类组件（`BasePageView`）执行 `retranslateUi` 逻辑，实现真正的无重启语言切换。

### 7.2 全局异常捕获与业务日志 (Telemetry)
- **方案**: 
  - 在 Service 层实现统一的异常适配器，将底层 OS 错误转化为业务含义明确的 `ApplicationError`。
  - 引入业务级日志，不只是记录 Traceback，而是记录“用户试图删除 [分类A]，由于其下存在连接点而受阻”这类带有上下文的操作日志。

### 7.3 SDK 化潜力 (Headless Support)
- **方案**: 确保所有 `src/core/services` 都不依赖任何 `PySide6` 组件。这使得核心逻辑未来可以轻松迁移到 CLI 工具或 Web 后台，实现逻辑的极致纯净。