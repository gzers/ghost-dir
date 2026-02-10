# 文档专业化优化计划

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

**日期**: 2026-02-10
**范围**: docs/ 全量文档体系
**目标**: 提升准确性、可维护性、可发现性与一致性

---

## 1. 问题摘要（基于当前文档现状）

- 架构与模块描述存在版本不一致与历史遗留内容，易导致实现偏差。
- 文档链接与结构存在断链或失配，影响导航与可信度。
- 关键用户路径文档不足（入门教程、故障排除、FAQ）。
- 发布与版本信息不一致（版本号、Release Notes 位置与命名）。
- 第三方参考材料与项目自有文档混杂，噪音较高。
- 文档元信息（负责人、更新时间、适用版本）缺失或不统一。

---

## 2. 目标（可验证）

- 架构与模块说明与当前代码结构一致，且具备单一事实来源（Single Source of Truth）。
- docs/ 内所有链接 0 断链，文档导航可从顶层 README 完整覆盖。
- 用户路径文档覆盖率提升：安装 + 快速上手 + 核心功能 + 故障排除。
- 发布文档与版本策略一致，并与实际 Release 产物路径对齐。
- 文档维护机制可执行：更新流程、检查脚本、责任归属清晰。

---

## 2.1 执行准则（以实际架构为准）

- 以 `src/` 当前实际目录与代码实现作为文档修订基线，不以历史文档为准。
- 历史文档允许滞后，但必须标注状态：`active`、`archived`、`obsolete`（过期待迁移）。
- 涉及架构描述的文档更新时，必须同步核对以下目录：`src/common`、`src/models`、`src/dao`、`src/drivers`、`src/services`、`src/gui`。
- 对旧结构术语（如 `core`、`data`、`utils`）执行治理策略：迁移到 archived 或加“历史版本说明”，不得在主导航中与现行架构并列展示。

---

## 3. 范围与非范围

### 范围
- docs/ 中现有文档的结构、内容、链接、版本一致性与专业化表达。
- 关键用户与开发者路径文档的补齐与统一。
- 发布与版本文档流程的对齐与模板标准化。

### 非范围
- 代码结构改造与功能重构。
- 设计稿或 UI 视觉资产的重新制作。
- 外部发布渠道运营（社媒/市场文案发布）。

---

## 4. 优化后目录结构（目标态）

```text
docs/
├── README.md                              # 文档总入口（唯一导航）
├── architecture/                          # 跨角色架构真相源（SSOT）
│   ├── README.md
│   ├── system-overview.md
│   ├── layering-and-dependencies.md
│   └── data-flow.md
├── user-docs/                             # 面向最终用户
│   ├── README.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── guides/
│   │   ├── configuration.md
│   │   └── category-manager.md
│   └── troubleshooting/
│       ├── faq.md
│       └── common-issues.md
├── developer-docs/                        # 面向开发者
│   ├── README.md
│   ├── architecture/                      # 开发者视角说明（引用 architecture/）
│   ├── development/
│   │   ├── standards/
│   │   │   ├── coding-standard.md
│   │   │   ├── ui-standard.md
│   │   │   └── i18n-standard.md
│   │   ├── planning/
│   │   │   ├── active/
│   │   │   └── archived/
│   │   ├── progress/
│   │   └── reports/
│   └── testing/
│       ├── guides/
│       ├── test-plans/
│       └── test-reports/
├── release/                               # 发布与版本管理
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── release-guide.md
│   ├── release-templates.md
│   └── notes/
│       └── vX.Y.Z.md
├── reference-docs/                        # 项目内部参考（轻量）
│   ├── README.md
│   ├── api/
│   └── technical-notes/
└── vendor/                                # 第三方资料归档（降噪）
    ├── README.md
    └── qfluentwidgets/
```

结构说明：
- `docs/README.md` 作为唯一主导航，其他目录 README 不再承担跨域跳转。
- `architecture/` 作为全项目架构真相源，`developer-docs/architecture/` 仅做工程化解读并回链。
- `vendor/` 用于承载第三方示例与静态资源，避免污染项目核心文档检索。

---

## 5. 工作流与里程碑

### 阶段 A：盘点与基线（1-2 天）
- 生成 docs/ 文档清单与归类表。
- 扫描并修复显性断链（README 与索引页）。
- 标注“过期/待更新/规划中”内容并建立待办列表。

### 阶段 B：架构与技术文档统一（2-4 天）
- 统一架构描述来源：确认主索引与唯一真相文档。
- 修正旧模块命名与路径（core/data/utils 等历史结构）。
- 补全“依赖约束/层级职责/数据流”的一致表述。

### 阶段 C：用户文档补齐（2-3 天）
- 补齐“快速开始教程”和“常见问题/故障排除”。
- 标准化安装/配置/功能指南模板与示例。
- 明确系统要求与兼容性信息（OS/权限/文件系统）。

### 阶段 D：发布与版本体系对齐（1-2 天）
- 统一 Release Notes 文件命名和存放位置。
- 对齐 CHANGELOG 与版本号策略。
- 增加“版本适用范围”标注（与文档版本一致）。

### 阶段 E：参考资料整理与去噪（1-2 天）
- 将第三方示例/资源移动到明确的 vendor 区域。
- 对外部依赖加 License 与来源说明。
- 减少参考文档对主导航的干扰。

---

## 6. 交付物清单

- 统一的 docs/ 导航与索引结构。
- 架构与模块文档修订版（含一致的模块命名与依赖约束）。
- 用户路径文档补齐（安装、快速上手、核心功能、FAQ）。
- 发布文档一致性修复（Release Notes 位置与模板统一）。
- 文档维护机制与检查清单（含链接检查脚本或流程）。

---

## 7. 验收标准

- docs/ 所有 README 与索引无断链。
- 架构文档描述与 src/ 实际结构一致，无旧模块残留。
- 用户文档可独立完成“安装 → 配置 → 使用核心功能”。
- 发布流程文档与实际版本号/产物路径一致。
- 新增或更新文档均包含“更新时间/适用版本/负责人”。

---

## 8. 风险与依赖

- 依赖当前代码结构的确认（防止文档先行与实现脱节）。
- 版本号与发布历史未统一可能影响文档可信度。
- 第三方文档迁移需确认许可证与归档策略。

---

## 9. 后续审批点

- 是否确认“架构文档唯一来源”与主索引位置。
- 是否确认目标态目录结构中 `vendor/` 的引入。
- 是否同意发布文档命名统一为 `release-guide.md` 与 `release-templates.md`。
- 是否需要增加自动化文档检查（CI 或脚本）。



