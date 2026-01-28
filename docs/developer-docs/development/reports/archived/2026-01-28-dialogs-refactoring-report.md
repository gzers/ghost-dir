# 对话框组件化重构工作报告

## 1. 任务概述
根据项目架构规范，将 `src/gui/dialogs` 目录下的所有单文件对话框窗口重构为独立的包（Package）结构，以提升代码的模块化程度。

## 2. 实施变更
### 2.1 目录结构调整
将所有 `*_dialog.py` 文件移动至对应的包目录下并重命名为 `dialog.py`：
- `add_link/`
- `batch_move/`
- `export_dialog/` (重命名避免与关键字冲突)
- `icon_picker/`
- `import_dialog/` (重命名避免与关键字冲突)
- `scan_wizard/`
- `template_edit/`
- `template_preview/`

### 2.2 核心逻辑增强
针对 `AddLinkDialog` 进行了深度重构：
- 提取 `TemplateTabWidget` 到 `add_link/widgets.py`。
- 提取 `CustomTabWidget` 到 `add_link/widgets.py`。
- 简化 `AddLinkDialog` (dialog.py) 为协调器，管理 Tab 页面切换。

### 2.3 兼容性修复
- 更新 `src/gui/dialogs/__init__.py` 统一导出所有对话框。
- 更新 `console_view.py` 中的硬编码导入路径。

## 3. 验证结果
- 所有新路径下的对话框均已在 `__init__.py` 中正确引用。
- 导入逻辑在 `console_view.py` 中已同步更新。
- 结构与 `category_manager` 保持高度一致。

---
**日期**: 2026-01-28  
**人员**: Antigravity AI
