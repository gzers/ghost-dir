# 配置系统架构规范

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

> **版本**: v2.1
> **最后更新**: 2026-02-10
> **状态**: 现状可用 + 持续优化

## 1. 设计目标

- 官方默认配置与用户运行时配置分离
- 首次运行自动初始化
- 兼容历史配置文件命名
- GUI 通过 Service 访问配置，降低耦合

## 2. 当前真实结构

```text
项目根目录/
├── config/                            # 官方模板（只读源）
│   ├── default_config.json
│   ├── default_categories.json
│   └── default_templates.json
├── src/common/config.py               # 路径与默认值定义 + 初始化逻辑
├── src/services/config_service.py     # 业务层配置服务
└── .ghost-dir/                        # 用户可读写配置目录
    ├── config.json
    ├── categories.json
    ├── templates.json
    └── links.json
```

打包后：
- 官方模板位于 `_internal/config/`
- 用户配置位于可执行文件同级 `.ghost-dir/`

## 3. 路径常量（代码基线）

路径定义位于 `src/common/config.py`，核心常量如下：
- `DEFAULT_CONFIG_FILE`
- `DEFAULT_CATEGORIES_FILE`
- `DEFAULT_TEMPLATES_FILE`
- `USER_CONFIG_FILE`
- `USER_CATEGORIES_FILE`
- `USER_TEMPLATES_FILE`
- `USER_LINKS_FILE`

## 4. 初始化与迁移

当前行为（`src/common/config.py`）：
1. 创建 `.ghost-dir` 与日志目录。
2. 若用户文件缺失，则从 `default_*.json` 复制到用户目录。
3. 自动迁移旧命名：
   - `user_config.json` -> `config.json`
   - `user_data.json` -> `links.json`

## 5. 分层访问规范

- GUI 层通过 `src/services/config_service.py` 访问配置。
- Service 层可调用 DAO 或直接使用 `src/common/config.py` 的路径常量。
- 禁止在 View 中散落文件读写逻辑。

## 6. 恢复默认策略（建议）

建议在 Service 层提供以下能力：
- 恢复全部默认配置（保留 `links.json`）
- 分项恢复（分类/模板/UI 配置）
- 恢复前自动备份

说明：
- 本文档只描述架构约束，不代表所有恢复能力已在当前版本实现。

## 7. 文档与实现一致性要求

- 文档中提到的模块路径必须存在于仓库。
- 若代码结构变更，优先更新 `src/common/config.py` 的说明，再同步本文件。
- 不再使用已失效路径示例（如 `src/core/services/...`）。

## 8. 相关文档

- [系统架构](./overview/system-architecture.md)
- [服务层架构](./overview/service-architecture-design.md)
- [标准化开发规约](../development/standardization-guide.md)
