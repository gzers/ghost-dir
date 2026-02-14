# Service 层架构设计（当前实现）

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 1. 目标

Service 层用于隔离 UI 与持久化/系统操作，统一承接业务规则、流程编排与状态更新。

## 2. 分层关系

```text
GUI (views/dialogs/components)
  -> Services
  -> DAO + Drivers
  -> Models/Common
```

规则：
- View 不直接持久化数据，不直接执行业务事务。
- Service 不直接操作具体 GUI 控件。

## 3. 现有服务清单

当前目录：`src/services/`

- `CategoryService`: 分类查询与增删改编排
- `TemplateService`: 模板查询、过滤与增删改
- `LinkService`: 链接状态、扫描并发、体积统计等流程
- `SmartScanner`（`scan_service.py`）: 扫描发现流程
- `ConfigService`: 配置读写封装
- `MigrationService`: 迁移流程服务
- `OccupancyService`: 占用/空间相关服务

## 4. 依赖规范

- Service 可以依赖 `src/dao`、`src/drivers`、`src/models`、`src/common`。
- Service 禁止依赖 `src/gui`。
- DAO/Drivers 禁止反向依赖 Service。

## 5. 交互示例

删除分类流程：
1. GUI 触发删除操作。
2. `CategoryService` 校验规则并调用 `CategoryDAO`。
3. 成功后通过全局信号通知视图刷新。

扫描流程：
1. GUI 发起扫描任务。
2. `SmartScanner` 基于模板与已管理链接做过滤。
3. GUI 根据回调/信号更新进度与结果。

## 6. 工程化约束

- 耗时逻辑放在 Service/Worker，不阻塞 UI 主线程。
- 跨模块通知使用 `src/common/signals.py`。
- 与系统相关的能力（文件、Windows API、事务）优先下沉到 Drivers。

## 7. 后续演进方向

- 逐步收敛兼容层（`service_bus`、`managers`）在新代码中的使用范围。
- 增强 Service 层可测试性：通过依赖注入替换 DAO/Drivers。
- 统一业务异常模型，减少 UI 对底层错误细节的感知。

**最后更新**: 2026-02-10
