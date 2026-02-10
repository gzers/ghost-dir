# 配置系统指南（当前实现）

本文档说明 Ghost-Dir 当前版本的配置文件结构、职责和常见维护方式。

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 配置职责划分

### `src/common/config.py`

职责：
- 定义应用常量（名称、版本、默认值）
- 统一配置文件路径
- 首次运行时初始化 `.ghost-dir` 用户配置
- 提供基础工具函数（如 `format_size`）

### `src/services/config_service.py`

职责：
- 提供业务侧配置读写入口
- 对 GUI 层隐藏底层持久化细节

### `src/dao/*.py`

职责：
- 负责分类、模板、链接等数据对象的 JSON 持久化读写

## 配置文件位置

开发环境：
- 官方模板：`config/default_config.json`、`config/default_categories.json`、`config/default_templates.json`
- 用户数据：`.ghost-dir/config.json`、`.ghost-dir/categories.json`、`.ghost-dir/templates.json`、`.ghost-dir/links.json`

打包环境：
- 官方模板在 `_internal/config/`
- 用户数据在可执行文件同级 `.ghost-dir/`

## 初始化与迁移

当前逻辑位于 `src/common/config.py`：
- 首次运行时，若用户配置不存在，则从 `default_*.json` 复制到 `.ghost-dir/`
- 兼容旧命名迁移：
  - `user_config.json` -> `config.json`
  - `user_data.json` -> `links.json`

## 关键默认值

示例（以代码为准）：
- `DEFAULT_THEME`
- `DEFAULT_THEME_COLOR`
- `DEFAULT_STARTUP_PAGE`
- `DEFAULT_LINK_VIEW`
- `DEFAULT_TARGET_DRIVE`
- `DEFAULT_TARGET_ROOT`

## 新增配置项建议流程

1. 在 `src/common/config.py` 增加默认值与可选项常量。
2. 在 `src/services/config_service.py` 增加对应读写方法。
3. 在 GUI 设置页卡片中接入该配置项。
4. 如需持久化结构变化，同步更新 `config/default_config.json`。

## 注意事项

- 不要在 GUI 组件中硬编码默认值，统一读取 `src/common/config.py`。
- 不要跨层直接从 View 访问 DAO 文件读写，统一经 Service 层收口。
- 文档中的配置键名与默认值若与代码冲突，以代码为准并及时回写文档。
