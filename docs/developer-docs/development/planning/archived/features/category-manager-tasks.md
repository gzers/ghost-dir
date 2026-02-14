# Category Manager 开发任务清单

- 适用版本: `>=1.0.0`
- 文档状态: `archived`
- 最后更新: `2026-02-10`

> [!WARNING]
> 本文档已归档，仅供追溯参考，不作为当前实施清单。
> 当前代码结构以 `src/services`、`src/dao`、`src/models`、`src/gui` 为准。

## 阶段 1: 后端增强 (Backend Enhancements)

### 1.1 数据模型扩展
- [x] 为 `CategoryNode` 添加 `order` 字段的批量更新方法
- [x] 在 `CategoryManager` 中实现 `reorder_categories()` 方法
- [x] 实现 `save_order_to_database()` (即 `save_categories`) 即时保存功能
- [x] 实现 `update_category_structure()` 支持跨层级移动持久化

### 1.2 验证逻辑
- [x] 确保删除操作的批量验证逻辑完整 (检查子孙分类和模板)
- [x] 添加重命名操作的唯一性验证 (同一父分类下)

---

## 阶段 2: UI 组件重构 (UI Component Refactoring)

### 2.1 工具栏设计 (CommandBar)
- [x] 创建单行 `CommandBar` 布局 (使用 QHBoxLayout 模拟)
- [x] 实现 **新建** 按钮 (Add Action)
  - [x] 默认可用状态
  - [x] 排序模式下禁用
- [x] 实现 **重命名** 按钮 (Rename Action)
  - [x] 默认禁用，仅当选中项数 == 1 时启用
  - [x] 连接 `itemSelectionChanged` 信号
- [x] 实现 **删除** 按钮 (Delete Action)
  - [x] 默认禁用，仅当复选框勾选数 > 0 时启用
  - [x] 连接 `itemChanged` 信号
- [x] 实现 **排序** 按钮 (Sort Toggle Button)
  - [x] 使用 `TogglePushButton`
  - [x] 实现 `toggled(bool)` 信号处理
  - [x] 按下时高亮显示且文本变为"退出排序"
- [x] 实现 **帮助** 按钮 (Help Action)
  - [x] 显示操作说明对话框

### 2.2 树形控件 (TreeWidget)
- [x] 配置 `TreeWidget` 基础属性
  - [x] 设置 `setEditTriggers(NoEditTriggers)` 禁用双击编辑
  - [x] 初始化时显示复选框
- [x] 实现拖拽功能
  - [x] 配置拖拽模式为 `InternalMove`
  - [x] 实现 `dropEvent` 处理逻辑 (通过 `CategoryTreeWidget` 包装)
- [x] 实现右键菜单
  - [x] 重命名 (F2)
  - [x] 在此新建
  - [x] 删除此项（忽略复选框）

---

## 阶段 3: 双模式交互逻辑 (Dual-Mode Interaction)

### 3.1 浏览模式 (Browse Mode - 默认)
- [x] 显示所有复选框
- [x] 启用新建/重命名/删除按钮（根据状态）
- [x] 禁用拖拽功能
- [x] 单击选中高亮，复选框用于删除

### 3.2 排序模式 (Sort Mode)
- [x] **进入排序模式**
  - [x] 隐藏所有复选框
  - [x] 禁用新建/重命名/删除按钮
  - [x] 启用拖拽功能
  - [x] 排序按钮高亮显示
- [x] **退出排序模式**
  - [x] 恢复显示复选框
  - [x] 恢复新建/重命名/删除按钮状态
  - [x] 禁用拖拽功能
  - [x] **立即保存新的结构与顺序到数据库**
  - [x] 排序按钮恢复正常

### 3.3 按钮状态管理
- [x] 实现 `_on_selection_changed` 处理重命名按钮
- [x] 实现 `_update_delete_button_state` 处理删除按钮
- [x] 排序模式下自动禁用所有编辑动作

---

## 阶段 4: 基础编辑功能实现 (Basic Edit Features)

### 4.1 新建分类
- [x] 在当前高亮行下创建子项
- [x] 无高亮则创建根项
- [x] 即时保存到数据库
- [x] 弹出输入对话框获取分类名称

### 4.2 重命名分类
- [x] 弹出输入对话框修改名称
- [x] 验证名称唯一性
- [x] 即时保存到数据库
- [x] 支持 F2 快捷键

### 4.3 删除分类
- [x] 弹出模态确认对话框
- [x] 显示将要删除的分类及其模板风险提示 (i18n 支持)
- [x] 批量删除勾选的分类
- [x] 即时保存到数据库

---

## 阶段 5: 排序功能实现 (Sorting Feature) ⭐ 重点突破

### 5.1 拖拽事件处理
- [x] 通过自定义 `CategoryTreeWidget` 拦截 `dragMoveEvent` 和 `dropEvent`
- [x] 跨层级移动支持 (捕捉新的 `parent_id`)

### 5.2 拖拽验证逻辑
- [x] 防止拖拽到自己 (Qt 内置)
- [x] 防止拖拽到自己的子孙节点 (递归验证)
- [x] 系统分类保护 (不允许作为子分类)
- [x] 验证目标父节点是否包含模板 (不可添加子分类)
- [x] 验证总深度限制 (MAX_CATEGORY_DEPTH = 3)

### 5.3 保存结构到数据库
- [x] 实现 `_save_current_order` 递归收集树结构
- [x] 调用 `category_manager.update_category_structure()`
- [x] 显示保存成功提示

### 5.4 视觉反馈
- [x] 实现拖拽手柄图标 `::` (使用 Unicode ⠿ 符号)

---

## 阶段 6: 操作日志功能 (Operation Logging) ✅ 已完成
 
- [x] 历史方案创建 `src/data/category_log.py`（当前实现为 `.ghost-dir/category_log.json`，路径常量见 `src/common/config.py`）
- [x] 集成日志记录到各操作方法

---

## 阶段 7: 样式与用户体验 (Styling & UX)

### 7.1 视觉设计
- [x] 应用 Fluent Design 样式 (qfluentwidgets)
- [x] 模式切换时的标题动态反馈
- [x] 排序模式下禁用对话框完成/取消按钮，防止意外中断

### 7.2 交互反馈
- [x] 操作成功/失败的 InfoBar 提示
- [x] 复杂的删除确认警告 (带模板统计)
- [x] 详尽的中文帮助指南 (i18n)

---

## 阶段 8: 测试与验证 (Testing & Verification)

### 8.1 单元/集成验证
- [x] 加载/保存配置文件正确
- [x] 跨层级移动后重启应用验证

---

## 阶段 9: 文档与优化 (Documentation & Optimization) ✅ 已完成
 
- [x] 代码注释完善
- [x] i18n 完整覆盖
- [x] 用户手册更新
