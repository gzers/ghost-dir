# 文档专业化治理进度快照（2026-02-10）

- 适用版本: `>=1.0.0`
- 文档状态: `report`
- 最后更新: `2026-02-10`

## 已完成

1. 架构事实对齐
- 主架构文档已统一到真实代码目录：`src/gui`、`src/services`、`src/dao`、`src/drivers`、`src/models`、`src/common`。
- 旧术语 `core/data/utils` 从主干文档移除，仅保留在迁移/历史说明中。

2. 发布文档命名统一
- `docs/release/guide.md` -> `docs/release/release-guide.md`
- `docs/release/templates.md` -> `docs/release/release-templates.md`
- 兼容占位文件已迁移至 `docs/release/archived/` 并完成归档标记。

3. 链接治理
- 全量扫描并修复 docs 内部相对链接。
- 当前断链数为 `0`。
- 审计报告：`docs/developer-docs/development/reports/current/2026-02-10-docs-link-check-report.md`

4. 元信息标准化
- 在主干文档补齐统一头部字段：
  - `适用版本`
  - `文档状态`
  - `最后更新`
- 覆盖范围包含 `docs/` 顶层入口、`developer-docs`、`user-docs`、`architecture`、`reference-docs`、`release`。

5. 状态治理落地
- 状态策略已写入 `docs/README.md` 与 `docs/reference-docs/README.md`。
- `planning/active/features` 历史计划已迁移至 `planning/archived/features` 并统一归档标识。
- `refactoring` 目录补齐索引并明确 active/archived 规则。

## 当前校验结果

- `docs/**/*.md` 内部链接断链数：`0`
- 非归档文档缺失 `文档状态`：`0`
- 计划目录（`development/planning`）非归档文档缺失 `文档状态`：`0`
- 非归档文档缺失任一头部字段（`适用版本/文档状态/最后更新`）：`0`
- docs 文档总量（当前快照）：`81`
- docs 内部相对链接总数（当前快照）：`232`
- docs 文档状态分布（非归档路径）：`active=45`、`report=4`、`external=6`、`missing=0`

## 待继续

1. 持续执行 docs 例行巡检（断链、状态字段、命名一致性）。

## 本轮新增完成

1. 已补齐 `development/`、`planning/`、`progress/`、`progress/current/`、`reports/`、`reports/current/`、`reports/current/active/` 的索引文档。
2. 已在 `docs/developer-docs/README.md` 增加对上述索引页的回链。
3. 已将 `planning/active/features` 的 4 个历史 `obsolete` 计划迁移到 `planning/archived/features` 并更新索引。
4. 已在 `docs/reference-docs/README.md` 新增“第三方外部参考”分区，并增加 `docs/reference-docs/external/README.md` 外部索引页。
5. 已清理 `ui-design`、`architecture`、`technical-notes` 中模板残留（`$status`、无效头部注入）并统一元信息格式。
6. 已完成 docs 全量内链复检：扫描 `81` 个 Markdown 文件、`232` 条内部相对链接，断链 `0`。
7. 已完成 docs 元信息完整性复检：非归档文档扫描 `55` 个，缺失任一头部字段 `0`。
8. 已完成剩余 `obsolete` 文档归档迁移（release/migration/refactoring），并补齐 `archived` 索引导航。
9. 已生成 docs 文档状态分布统计报告（全量与非归档路径双视角）。
10. 已补齐 archived 历史文档元信息头部字段，完成全量文档状态字段收口（missing=0）。
