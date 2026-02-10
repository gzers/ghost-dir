# Ghost-Dir 文档中心

本目录是项目文档统一入口。文档更新遵循“代码事实优先”原则：架构描述以 `src/` 当前实际目录为准。

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 文档导航

- [架构文档](architecture/README.md): 系统分层、依赖规则、数据流与设计约束
- [开发文档](developer-docs/README.md): 开发规约、架构说明、测试与实施计划
- [用户文档](user-docs/README.md): 安装、配置、功能使用与问题排查
- [参考文档](reference-docs/README.md): UI 规范、技术笔记、参考资料
- [发布文档](release/README.md): 发布流程、更新日志、发布说明模板
- [迁移文档](migration/README.md): 架构与模块迁移文档

## 当前代码架构（以 src 实际目录为准）

```text
src/
├── gui/         # 表现层：窗口、页面、组件、对话框、样式、国际化
├── services/    # 业务层：编排业务流程，协调 DAO 与 Drivers
├── dao/         # 数据访问层：JSON 持久化读写与查询
├── drivers/     # 系统驱动层：文件系统、事务、Windows 能力封装
├── models/      # 数据模型层：实体定义与序列化
└── common/      # 基础层：配置、异常、信号、验证器、兼容层
```

## docs 目录结构（全量中文注释）

```text
docs/
├── README.md                                           # 文档中心入口（本文件）
├── architecture/                                       # 跨角色架构总览文档
│   └── README.md                                       # 五层架构、职责、依赖与最佳实践
├── developer-docs/                                     # 开发者文档总目录
│   ├── README.md                                       # 开发文档导航
│   ├── i18n-guide.md                                   # 国际化开发指南
│   ├── architecture/                                   # 开发者视角架构文档
│   │   ├── README.md                                   # 架构文档索引
│   │   ├── config-system.md                            # 配置系统架构规范
│   │   ├── data-flow/                                  # 数据流设计
│   │   │   └── data-flow-diagram.md                    # 业务数据流图
│   │   ├── design-patterns/                            # 设计模式
│   │   │   └── patterns-used.md                        # 已使用模式说明
│   │   └── overview/                                   # 架构概览与模块说明
│   │       ├── component-architecture.md               # GUI 组件架构
│   │       ├── core-modules.md                         # 模块详解（含历史内容，待治理）
│   │       ├── service-architecture-design.md          # 服务层设计说明
│   │       └── system-architecture.md                  # 系统架构总览
│   ├── contributing/                                   # 贡献相关文档目录（预留）
│   ├── design/                                         # 设计规范
│   │   └── UI_DESIGN_STANDARDS.md                      # UI 设计标准
│   ├── development/                                    # 开发过程文档
│   │   ├── pyqt-threading-best-practices.md            # PyQt 线程最佳实践
│   │   ├── standardization-guide.md                    # 标准化开发规约
│   │   ├── planning/                                   # 规划文档
│   │   │   ├── active/                                 # 当前进行中的计划
│   │   │   └── archived/                               # 历史计划归档
│   │   ├── progress/                                   # 开发进度文档
│   │   ├── reports/                                    # 实施报告文档
│   │   ├── setup/                                      # 开发环境搭建文档
│   │   └── testing/                                    # 开发阶段测试材料
│   └── testing/                                        # 测试文档总目录
│       ├── guides/                                     # 测试指南
│       ├── test-plans/                                 # 测试计划
│       └── test-reports/                               # 测试报告
├── migration/                                          # 架构/模块迁移记录
│   ├── README.md                                       # 迁移文档索引
│   └── archived/                                       # 历史迁移文档归档
│       └── gui-migration-summary.md                    # GUI 迁移总结（归档）
├── reference-docs/                                     # 参考资料（含第三方内容）
│   ├── README.md                                       # 参考文档导航
│   ├── api/                                            # API 参考（目录已建）
│   ├── technical-notes/                                # 技术笔记
│   │   └── ui/pages/base-page-readme.md                # 基础页面技术说明
│   └── ui-design/                                      # UI 设计参考
│       ├── components/                                 # 组件参考（含 qfluent-widgets 示例）
│       └── typography/                                 # 排版规范
├── release/                                            # 发布与版本文档
│   ├── README.md                                       # 发布文档导航
│   ├── CHANGELOG.md                                    # 版本更新日志
│   ├── release-guide.md                                # 发布流程指南
│   ├── release-templates.md                            # 发布文案模板
│   ├── archived/                                       # 历史发布文档归档
│   └── notes/                                          # 版本发布说明
│       └── v1.0.0.md                                   # 1.0.0 版本说明
└── user-docs/                                          # 用户文档总目录
    ├── README.md                                       # 用户文档导航
    ├── getting-started/                                # 入门文档
    │   └── installation/install.md                     # 安装说明
    └── user-guide/                                     # 功能与配置指南
        ├── configuration/configuration-guide.md        # 配置系统指南
        └── features/category-manager.md                # 分类管理指南
```

## 文档维护规则

- 架构相关文档更新时，必须同步核对 `src/common`、`src/models`、`src/dao`、`src/drivers`、`src/services`、`src/gui`。
- 历史结构术语（如 `core/data/utils`）只允许出现在归档文档或“历史说明”中。
- 所有 README 与索引页面必须保证相对链接可访问，禁止保留无效引用。

### 状态策略

- `active`: 当前维护中的主文档。
- `report`: 检查/审计输出文档。
- `external`: 第三方镜像文档，仅用于参考，默认不做内容改写。
- `obsolete`: 已过期文档，保留历史价值但不作为实施依据。
