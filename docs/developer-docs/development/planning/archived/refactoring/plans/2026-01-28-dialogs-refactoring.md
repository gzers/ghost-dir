# 对话框组件化重构计划

- 适用版本: `7.x 历史阶段`
- 文档状态: `archived`
- 最后更新: `2026-02-10`

## 目标
将 `src/gui/dialogs` 目录下的所有单文件对话框重构为包（Package）结构，以保持与 `category_manager` 一致的架构。

## 重构列表及进度
- [x] `add_link_dialog.py` -> `add_link/`
- [x] `batch_move_dialog.py` -> `batch_move/`
- [x] `export_dialog.py` -> `export_dialog/` (重命名避免冲突)
- [x] `icon_picker_dialog.py` -> `icon_picker/`
- [x] `import_dialog.py` -> `import_dialog/` (重命名避免冲突)
- [x] `scan_wizard_dialog.py` -> `scan_wizard/`
- [x] `template_edit_dialog.py` -> `template_edit/`
- [x] `template_preview_dialog.py` -> `template_preview/`

## 步骤模板
1. 创建文件夹 `src/gui/dialogs/{name}`。
2. 创建 `src/gui/dialogs/{name}/__init__.py`。
3. 将 `{name}_dialog.py` 移动并重命名为 `src/gui/dialogs/{name}/dialog.py`。
4. 更新内部相对导入（如果有 `from . import ...`）。
5. 更新 `src/gui/dialogs/__init__.py` 的导出。
6. 全局搜索并替换该对话框的引用路径。
