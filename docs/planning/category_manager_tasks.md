# Category Manager 开发任务清单

## 阶段 1: 后端增强 (Backend Enhancements)

### 1.1 数据模型扩展
- [ ] 为 `CategoryNode` 添加 `order` 字段的批量更新方法
- [ ] 在 `CategoryManager` 中实现 `reorder_categories()` 方法
- [ ] 实现 `save_order_to_database()` 即时保存功能

### 1.2 验证逻辑
- [ ] 确保删除操作的批量验证逻辑完整
- [ ] 添加重命名操作的唯一性验证

---

## 阶段 2: UI 组件重构 (UI Component Refactoring)

### 2.1 工具栏设计 (CommandBar)
- [ ] 创建单行 `CommandBar` 布局
- [ ] 实现 **新建** 按钮 (Add Action)
  - [ ] 默认可用状态
  - [ ] 排序模式下禁用
- [ ] 实现 **重命名** 按钮 (Rename Action)
  - [ ] 默认禁用，仅当选中项数 == 1 时启用
  - [ ] 连接 `itemSelectionChanged` 信号
- [ ] 实现 **删除** 按钮 (Delete Action)
  - [ ] 默认禁用，仅当复选框勾选数 > 0 时启用
  - [ ] 连接 `itemChanged` 信号
- [ ] 实现 **排序** 按钮 (Sort Toggle Button)
  - [ ] 设置为 `checkable=True`
  - [ ] 实现 `toggled(bool)` 信号处理
  - [ ] 按下时高亮显示（Pressed State）
- [ ] 实现 **帮助** 按钮 (Help Action)
  - [ ] 显示 TeachingTip 操作说明

### 2.2 树形控件 (TreeWidget)
- [ ] 配置 `TreeWidget` 基础属性
  - [ ] 设置 `setEditTriggers(NoEditTriggers)` 禁用双击编辑
  - [ ] 初始化时显示复选框
- [ ] 实现拖拽功能
  - [ ] 配置拖拽模式为 `InternalMove`
  - [ ] 实现 `dropEvent` 处理逻辑
- [ ] 实现右键菜单
  - [ ] 重命名 (F2)
  - [ ] 在此新建
  - [ ] 删除此项（忽略复选框）

---

## 阶段 3: 双模式交互逻辑 (Dual-Mode Interaction)

### 3.1 浏览模式 (Browse Mode - 默认)
- [ ] 显示所有复选框
- [ ] 启用新建/重命名/删除按钮（根据状态）
- [ ] 禁用拖拽功能 (`setDragEnabled(False)`)
- [ ] 单击选中高亮，复选框用于删除

### 3.2 排序模式 (Sort Mode)
- [ ] **进入排序模式**
  - [ ] 隐藏所有复选框（或替换为拖拽手柄图标 `::`）
  - [ ] 禁用新建/重命名/删除按钮
  - [ ] 启用拖拽功能 (`setDragEnabled(True)`)
  - [ ] 排序按钮高亮显示
- [ ] **退出排序模式**
  - [ ] 恢复显示复选框
  - [ ] 恢复新建/重命名/删除按钮状态
  - [ ] 禁用拖拽功能
  - [ ] **立即保存新的顺序到数据库**
  - [ ] 排序按钮恢复透明

### 3.3 按钮状态管理
- [ ] 实现 `updateRenameButtonState()` 槽函数
  - [ ] 逻辑: `len(selectedItems) == 1`
- [ ] 实现 `updateDeleteButtonState()` 槽函数
  - [ ] 逻辑: `countCheckedItems() > 0`
- [ ] 实现 `updateAddButtonState()` 槽函数
  - [ ] 排序模式下禁用，其他时候可用

---

## 阶段 4: 基础编辑功能实现 (Basic Edit Features)

### 4.1 新建分类
- [ ] 在当前高亮行下创建子项
- [ ] 无高亮则创建根项
- [ ] 即时保存到数据库
- [ ] 弹出输入对话框获取分类名称

### 4.2 重命名分类
- [ ] 弹出输入对话框修改名称
- [ ] 验证名称唯一性
- [ ] 即时保存到数据库
- [ ] 支持 F2 快捷键

### 4.3 删除分类
- [ ] 弹出模态确认对话框
- [ ] 显示将要删除的分类数量
- [ ] 批量删除勾选的分类
- [ ] 即时保存到数据库

---

## 阶段 5: 排序功能实现 (Sorting Feature) ⭐ 独立步骤

### 5.1 拖拽事件处理
- [ ] 实现 `_on_drop_event()` 方法
- [ ] 获取拖拽的项和目标位置
- [ ] 处理拖拽操作

### 5.2 拖拽验证逻辑
- [ ] 实现 `_validate_drag()` 方法
- [ ] 防止拖拽到自己
- [ ] 防止拖拽到自己的子孙节点
- [ ] 系统分类不可移动

### 5.3 保存排序到数据库
- [ ] 实现 `_save_current_order()` 方法
- [ ] 递归收集所有分类的新 order
- [ ] 调用 `category_manager.reorder_categories()`
- [ ] 显示保存成功提示

### 5.4 排序模式视觉反馈（可选）
- [ ] 实现拖拽手柄图标 `::`
- [ ] 在排序模式下显示手柄
- [ ] 退出排序模式时隐藏手柄

---

## 阶段 6: 操作日志功能 (Operation Logging) 📝 可选功能

### 6.1 日志数据模型
- [ ] 创建 `src/data/category_log.py`
- [ ] 定义 `CategoryOperation` 枚举
- [ ] 定义 `CategoryLogEntry` 数据类

### 6.2 日志管理器
- [ ] 在 `CategoryManager` 中添加日志相关方法
- [ ] 实现 `_load_logs()` 方法
- [ ] 实现 `_save_logs()` 方法
- [ ] 实现 `_log_operation()` 方法
- [ ] 实现 `get_recent_logs()` 方法

### 6.3 集成日志记录
- [ ] 在 `add_category()` 中记录日志
- [ ] 在 `rename_category()` 中记录日志
- [ ] 在 `delete_category()` 中记录日志
- [ ] 在 `reorder_categories()` 中记录日志

### 6.4 日志查看界面（可选）
- [ ] 在设置页面添加日志查看功能
- [ ] 显示最近 50 条操作记录
- [ ] 支持按操作类型筛选

---

## 阶段 7: 样式与用户体验 (Styling & UX)

### 7.1 视觉设计
- [ ] 应用 Fluent Design 样式
- [ ] 排序按钮的高亮效果（Pressed State）
- [ ] 拖拽手柄图标设计（可选）
- [ ] 复选框的显示/隐藏动画（可选）

### 7.2 交互反馈
- [ ] 操作成功/失败的 Toast 提示
- [ ] 删除确认对话框的样式优化
- [ ] TeachingTip 帮助提示的内容编写

---

## 阶段 8: 测试与验证 (Testing & Verification)

### 8.1 功能测试
- [ ] 测试新建分类（根项、子项）
- [ ] 测试重命名分类（F2、右键菜单）
- [ ] 测试删除分类（单个、批量）
- [ ] 测试排序功能（同级、跨级）

### 8.2 模式切换测试
- [ ] 测试浏览模式 → 排序模式切换
- [ ] 测试排序模式 → 浏览模式切换
- [ ] 验证按钮状态正确更新
- [ ] 验证复选框显示/隐藏

### 8.3 边界条件测试
- [ ] 测试空列表状态
- [ ] 测试系统分类保护（不可删除）
- [ ] 测试最大深度限制
- [ ] 测试拖拽到非法位置

### 8.4 数据持久化测试
- [ ] 验证即时保存功能
- [ ] 验证重启应用后数据正确加载
- [ ] 验证排序后的 order 字段正确保存

---

## 阶段 9: 文档与优化 (Documentation & Optimization)

### 9.1 代码文档
- [ ] 添加详细的类和方法注释
- [ ] 编写 UI 交互流程说明

### 9.2 性能优化
- [ ] 优化大量分类时的渲染性能
- [ ] 优化拖拽操作的流畅度

### 9.3 用户文档
- [ ] 更新用户手册中的分类管理章节
- [ ] 添加操作截图和动画演示
