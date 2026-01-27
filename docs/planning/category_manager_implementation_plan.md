# Category Manager 功能重构实施方案

## 概述

根据 PRD 要求，将现有的分类管理对话框重构为具有**双模式隔离**的现代化界面：
- **浏览模式**（默认）：用于日常的增删改操作
- **排序模式**：专门用于拖拽调整分类顺序和层级

核心设计理念：
1. **单行工具栏**：极致节省空间，所有操作集中在顶部 CommandBar
2. **模式隔离**：将"增删改"与"排序"彻底分离，防止误操作
3. **即时保存**：无底部确认按钮，所有操作立即写入数据库
4. **纯单击交互**：禁用双击，所有操作通过按钮或右键完成

---

## 用户审查要点

> [!IMPORTANT]
> **破坏性变更**
> 
> 1. **移除底部输入框**：原有的"输入新分类名称"输入框和"添加根分类"按钮将被移除，新建操作改为通过顶部工具栏完成
> 2. **即时保存机制**：所有操作（新建、重命名、删除、排序）将立即保存到数据库，无需点击"完成"按钮确认
> 3. **双击编辑禁用**：禁用双击重命名功能，改为通过工具栏"重命名"按钮或 F2 快捷键触发

> [!WARNING]
> **UI 交互变更**
> 
> 1. **复选框用途变更**：复选框仅用于批量删除，不再用于其他操作
> 2. **排序模式独占**：进入排序模式后，所有编辑按钮将被禁用，只能进行拖拽操作
> 3. **右键菜单新增**：新增右键菜单，提供"重命名"、"在此新建"、"删除此项"快捷操作

---

## 实施变更

### 阶段 1: 后端增强

#### 1.1 [MODIFY] [category_manager.py](file:///d:/Users/15119/WorkSpace/Code/tool/ghost-dir/src/data/category_manager.py)

**新增方法**：
- `reorder_categories(category_orders: List[Tuple[str, int]]) -> Tuple[bool, str]`
  - 批量更新分类的 `order` 字段
  - 参数：`[(category_id, new_order), ...]`
  - 立即保存到数据库
  - 返回：`(是否成功, 消息)`

- `rename_category(category_id: str, new_name: str) -> Tuple[bool, str]`
  - 重命名分类
  - 验证名称唯一性（同一父分类下）
  - 立即保存到数据库
  - 返回：`(是否成功, 消息)`

**修改方法**：
- `save_categories()` - 确保保存时按 `order` 字段排序

---

### 阶段 2: UI 组件重构

#### 2.1 [MODIFY] [category_manager.py](file:///d:/Users/15119/WorkSpace/Code/tool/ghost-dir/src/gui/dialogs/category_manager.py)

**完全重构 UI 布局**：

##### 顶部工具栏 (CommandBar)
```python
# 使用 QHBoxLayout 创建单行工具栏
toolbar_layout = QHBoxLayout()

# 左侧编辑按钮组
add_action = QAction(FluentIcon.ADD, "新建")
rename_action = QAction(FluentIcon.EDIT, "重命名")
delete_action = QAction(FluentIcon.DELETE, "删除")

# 分隔符
toolbar_layout.addStretch()

# 右侧功能按钮
sort_action = QAction(FluentIcon.SORT, "排序")
sort_action.setCheckable(True)  # 设置为可切换按钮
help_action = QAction(FluentIcon.HELP, "帮助")
```

##### 树形控件配置
```python
self.categoryTree.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁用双击编辑
self.categoryTree.setDragDropMode(QAbstractItemView.NoDragDrop)  # 初始禁用拖拽
self.categoryTree.setSelectionMode(QAbstractItemView.SingleSelection)
```

##### 移除的组件
- 底部输入框 (`nameEdit`)
- "添加根分类" 按钮 (`addButton`)
- "添加子分类" 按钮 (`addChildButton`)
- "全部展开/折叠" 按钮（可选保留在右键菜单）

---

### 阶段 3: 双模式交互逻辑

#### 3.1 浏览模式（默认）

**状态特征**：
- 显示所有复选框
- 新建按钮：始终可用
- 重命名按钮：仅当选中项数 == 1 时可用
- 删除按钮：仅当复选框勾选数 > 0 时可用
- 排序按钮：未按下（透明背景）
- 拖拽功能：禁用

**实现**：
```python
def _enter_browse_mode(self):
    """进入浏览模式"""
    # 恢复复选框显示
    self._set_checkboxes_visible(True)
    
    # 禁用拖拽
    self.categoryTree.setDragEnabled(False)
    self.categoryTree.setAcceptDrops(False)
    
    # 恢复按钮状态
    self.add_action.setEnabled(True)
    self._update_rename_button_state()
    self._update_delete_button_state()
    
    # 排序按钮恢复未按下状态
    self.sort_action.setChecked(False)
```

#### 3.2 排序模式

**状态特征**：
- 隐藏所有复选框（或替换为拖拽手柄图标 `::`）
- 新建/重命名/删除按钮：全部禁用
- 排序按钮：按下状态（高亮背景）
- 拖拽功能：启用

**实现**：
```python
def _enter_sort_mode(self):
    """进入排序模式"""
    # 隐藏复选框
    self._set_checkboxes_visible(False)
    
    # 启用拖拽
    self.categoryTree.setDragEnabled(True)
    self.categoryTree.setAcceptDrops(True)
    self.categoryTree.setDragDropMode(QAbstractItemView.InternalMove)
    
    # 禁用所有编辑按钮
    self.add_action.setEnabled(False)
    self.rename_action.setEnabled(False)
    self.delete_action.setEnabled(False)
    
    # 排序按钮设置为按下状态
    self.sort_action.setChecked(True)

def _exit_sort_mode(self):
    """退出排序模式"""
    # 保存新的排序到数据库
    self._save_current_order()
    
    # 返回浏览模式
    self._enter_browse_mode()
```

#### 3.3 模式切换信号处理

```python
def _on_sort_toggled(self, checked: bool):
    """排序按钮切换"""
    if checked:
        self._enter_sort_mode()
    else:
        self._exit_sort_mode()
```

---

### 阶段 4: 基础编辑功能实现 (Basic Edit Features)

#### 4.1 新建分类

**触发方式**：
- 点击工具栏"新建"按钮
- 右键菜单"在此新建"

**逻辑**：
```python
def _on_add_category(self):
    """新建分类"""
    selected_items = self.categoryTree.selectedItems()
    
    # 弹出输入对话框
    from qfluentwidgets import InputDialog
    dialog = InputDialog("新建分类", "请输入分类名称：", self)
    
    if dialog.exec():
        name = dialog.textValue().strip()
        if not name:
            return
        
        # 确定父分类
        parent_id = None
        if selected_items:
            parent_category = selected_items[0].data(0, Qt.UserRole)
            parent_id = parent_category.id
        
        # 创建分类
        category = CategoryNode(
            id=f"cat_{uuid.uuid4().hex[:8]}",
            name=name,
            parent_id=parent_id,
            order=self._get_next_order(parent_id)
        )
        
        # 添加并立即保存
        success, msg = self.category_manager.add_category(category)
        
        if success:
            self._load_categories()
            self.categories_changed.emit()
            InfoBar.success(title='成功', content=msg, parent=self)
        else:
            MessageBox("失败", msg, self).exec()
```

#### 4.2 重命名分类

**触发方式**：
- 点击工具栏"重命名"按钮
- 按 F2 快捷键
- 右键菜单"重命名"

**逻辑**：
```python
def _on_rename_category(self):
    """重命名分类"""
    selected_items = self.categoryTree.selectedItems()
    if not selected_items:
        return
    
    item = selected_items[0]
    category = item.data(0, Qt.UserRole)
    
    # 弹出输入对话框
    from qfluentwidgets import InputDialog
    dialog = InputDialog("重命名分类", "请输入新名称：", self)
    dialog.setTextValue(category.name)
    
    if dialog.exec():
        new_name = dialog.textValue().strip()
        if not new_name or new_name == category.name:
            return
        
        # 调用后端重命名方法
        success, msg = self.category_manager.rename_category(category.id, new_name)
        
        if success:
            self._load_categories()
            self.categories_changed.emit()
            InfoBar.success(title='成功', content=msg, parent=self)
        else:
            MessageBox("失败", msg, self).exec()
```

#### 4.3 删除分类

**触发方式**：
- 点击工具栏"删除"按钮（批量删除勾选项）
- 右键菜单"删除此项"（仅删除当前项）

**逻辑**：
```python
def _on_delete_category(self):
    """删除勾选的分类"""
    checked_categories = []
    self._collect_checked_items(self.categoryTree.invisibleRootItem(), checked_categories)
    
    if not checked_categories:
        return
    
    # 弹出确认对话框（保留现有逻辑）
    # ... 现有的删除逻辑 ...
```

---

### 阶段 5: 排序功能实现 (Sorting Feature)

> [!IMPORTANT]
> **独立实施阶段**
> 
> 排序功能影响较大，作为独立步骤实施。该功能涉及拖拽交互、顺序持久化、以及与现有树形结构的深度集成。

#### 5.1 拖拽事件处理

**实现拖拽排序逻辑**：
```python
def _on_drop_event(self, event):
    """处理拖拽放置事件"""
    # 获取拖拽的项和目标位置
    source_item = self.categoryTree.currentItem()
    target_item = self.categoryTree.itemAt(event.pos())
    
    if not source_item or not target_item:
        return
    
    # 获取分类数据
    source_category = source_item.data(0, Qt.UserRole)
    target_category = target_item.data(0, Qt.UserRole)
    
    # 验证拖拽合法性
    if not self._validate_drag(source_category, target_category):
        event.ignore()
        return
    
    # 执行拖拽操作
    event.accept()
    
    # 更新 order 字段会在退出排序模式时统一处理
```

#### 5.2 保存排序到数据库

**批量更新 order 字段**：
```python
def _save_current_order(self):
    """保存当前排序"""
    category_orders = []
    
    # 递归遍历树，收集所有分类的新 order
    def collect_orders(parent_item, parent_id):
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            category = child.data(0, Qt.UserRole)
            category_orders.append((category.id, i))
            # 递归处理子分类
            collect_orders(child, category.id)
    
    collect_orders(self.categoryTree.invisibleRootItem(), None)
    
    # 批量更新到数据库
    success, msg = self.category_manager.reorder_categories(category_orders)
    
    if success:
        InfoBar.success(title='成功', content='排序已保存', parent=self)
    else:
        MessageBox("失败", msg, self).exec()
```

#### 5.3 拖拽验证逻辑

**防止非法拖拽**：
```python
def _validate_drag(self, source: CategoryNode, target: CategoryNode) -> bool:
    """验证拖拽操作是否合法"""
    # 1. 不能拖拽到自己
    if source.id == target.id:
        return False
    
    # 2. 不能拖拽到自己的子孙节点
    if self._is_descendant(source.id, target.id):
        return False
    
    # 3. 系统分类不可移动
    if source.is_builtin:
        return False
    
    return True

def _is_descendant(self, ancestor_id: str, descendant_id: str) -> bool:
    """检查是否为子孙关系"""
    current_id = descendant_id
    while current_id:
        category = self.category_manager.get_category_by_id(current_id)
        if not category:
            break
        if category.parent_id == ancestor_id:
            return True
        current_id = category.parent_id
    return False
```

#### 5.4 排序模式视觉反馈

**拖拽手柄图标（可选）**：
```python
def _set_drag_handles_visible(self, visible: bool):
    """显示/隐藏拖拽手柄图标"""
    def update_item(item):
        if visible:
            # 在文本前添加 :: 图标
            category = item.data(0, Qt.UserRole)
            item.setText(0, f":: {category.name}")
        else:
            # 恢复原始文本
            category = item.data(0, Qt.UserRole)
            item.setText(0, category.name)
        
        # 递归处理子项
        for i in range(item.childCount()):
            update_item(item.child(i))
    
    root = self.categoryTree.invisibleRootItem()
    for i in range(root.childCount()):
        update_item(root.child(i))
```

---

### 阶段 6: 操作日志功能 (Operation Logging)

> [!NOTE]
> **可选功能**
> 
> 由于采用即时保存机制，添加操作日志可以帮助用户追踪分类变更历史，并在必要时进行回溯。

#### 6.1 日志数据模型

**新建日志文件**：`src/data/category_log.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class CategoryOperation(Enum):
    """分类操作类型"""
    CREATE = "create"
    RENAME = "rename"
    DELETE = "delete"
    REORDER = "reorder"
    MOVE = "move"  # 跨层级移动

@dataclass
class CategoryLogEntry:
    """分类操作日志条目"""
    timestamp: str
    operation: CategoryOperation
    category_id: str
    category_name: str
    details: Optional[dict] = None  # 额外信息，如旧名称、新父分类等
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "operation": self.operation.value,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CategoryLogEntry':
        return cls(
            timestamp=data["timestamp"],
            operation=CategoryOperation(data["operation"]),
            category_id=data["category_id"],
            category_name=data["category_name"],
            details=data.get("details")
        )
```

#### 6.2 日志管理器

**扩展 CategoryManager**：

```python
class CategoryManager:
    def __init__(self):
        # ... 现有代码 ...
        self.log_file = DATA_DIR / "category_log.json"
        self.logs: List[CategoryLogEntry] = []
        self._load_logs()
    
    def _load_logs(self):
        """加载操作日志"""
        if not self.log_file.exists():
            return
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logs = [CategoryLogEntry.from_dict(item) for item in data]
        except Exception as e:
            print(f"加载日志失败: {e}")
    
    def _save_logs(self):
        """保存操作日志"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                data = [log.to_dict() for log in self.logs]
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存日志失败: {e}")
    
    def _log_operation(self, operation: CategoryOperation, category: CategoryNode, details: dict = None):
        """记录操作日志"""
        entry = CategoryLogEntry(
            timestamp=datetime.now().isoformat(),
            operation=operation,
            category_id=category.id,
            category_name=category.name,
            details=details
        )
        self.logs.append(entry)
        self._save_logs()
    
    def get_recent_logs(self, limit: int = 50) -> List[CategoryLogEntry]:
        """获取最近的操作日志"""
        return self.logs[-limit:]
```

#### 6.3 集成日志记录

**在关键操作中添加日志**：

```python
# 在 add_category 方法中
def add_category(self, category: CategoryNode) -> Tuple[bool, str]:
    # ... 现有逻辑 ...
    if success:
        self._log_operation(CategoryOperation.CREATE, category)
    return success, msg

# 在 rename_category 方法中
def rename_category(self, category_id: str, new_name: str) -> Tuple[bool, str]:
    old_category = self.get_category_by_id(category_id)
    # ... 重命名逻辑 ...
    if success:
        self._log_operation(
            CategoryOperation.RENAME,
            category,
            details={"old_name": old_category.name, "new_name": new_name}
        )
    return success, msg

# 在 delete_category 方法中
def delete_category(self, category_id: str) -> Tuple[bool, str]:
    category = self.get_category_by_id(category_id)
    # ... 删除逻辑 ...
    if success:
        self._log_operation(CategoryOperation.DELETE, category)
    return success, msg
```

#### 6.4 日志查看界面（可选）

**在设置页面添加日志查看功能**：

- 显示最近 50 条操作记录
- 支持按操作类型筛选
- 显示时间、操作类型、分类名称、详细信息

---

### 阶段 7: 右键菜单

#### 5.1 实现右键菜单

```python
def _show_context_menu(self, pos):
    """显示右键菜单"""
    item = self.categoryTree.itemAt(pos)
    if not item:
        return
    
    menu = QMenu(self)
    
    # 重命名
    rename_action = QAction(FluentIcon.EDIT, "重命名 (F2)", self)
    rename_action.triggered.connect(self._on_rename_category)
    menu.addAction(rename_action)
    
    # 在此新建
    add_child_action = QAction(FluentIcon.ADD, "在此新建", self)
    add_child_action.triggered.connect(self._on_add_category)
    menu.addAction(add_child_action)
    
    menu.addSeparator()
    
    # 删除此项
    delete_action = QAction(FluentIcon.DELETE, "删除此项", self)
    delete_action.triggered.connect(lambda: self._delete_single_category(item))
    menu.addAction(delete_action)
    
    menu.exec(self.categoryTree.viewport().mapToGlobal(pos))
```

---

### 阶段 8: 帮助系统

#### 6.1 TeachingTip 实现

```python
def _show_help(self):
    """显示帮助提示"""
    from qfluentwidgets import TeachingTip, InfoBarIcon
    
    TeachingTip.create(
        target=self.help_button,
        icon=InfoBarIcon.INFORMATION,
        title="分类管理操作指南",
        content=(
            "• 单击选中分类，复选框用于批量删除\n"
            "• 按 F2 或点击重命名按钮编辑分类名称\n"
            "• 点击排序按钮进入拖拽模式调整顺序\n"
            "• 右键分类可快速访问常用操作"
        ),
        isClosable=True,
        tailPosition=TeachingTip.Position.BOTTOM,
        duration=5000,
        parent=self
    )
```

---

## 验证计划

### 自动化测试

由于该项目目前没有单元测试框架，本次不添加自动化测试。

### 手动验证

#### 测试 1: 浏览模式基础操作

**步骤**：
1. 运行应用：`python run.py`
2. 打开分类管理对话框
3. 验证默认状态：
   - [ ] 复选框可见
   - [ ] 新建按钮可用
   - [ ] 重命名按钮禁用（无选中项）
   - [ ] 删除按钮禁用（无勾选项）
   - [ ] 排序按钮未按下
4. 点击"新建"按钮，输入"测试分类1"
   - [ ] 弹出输入对话框
   - [ ] 输入后立即保存并显示在树中
5. 选中"测试分类1"，点击"重命名"
   - [ ] 重命名按钮变为可用
   - [ ] 弹出输入对话框，修改为"测试分类A"
   - [ ] 立即保存并更新显示
6. 勾选"测试分类A"的复选框
   - [ ] 删除按钮变为可用
7. 点击"删除"按钮
   - [ ] 弹出确认对话框
   - [ ] 确认后立即删除

#### 测试 2: 排序模式操作

**步骤**：
1. 创建 3 个根分类："分类1"、"分类2"、"分类3"
2. 点击"排序"按钮
   - [ ] 排序按钮高亮显示（按下状态）
   - [ ] 复选框消失或变为拖拽手柄
   - [ ] 新建/重命名/删除按钮全部禁用
3. 拖拽"分类3"到"分类1"上方
   - [ ] 拖拽操作流畅
   - [ ] 顺序变为："分类3"、"分类1"、"分类2"
4. 再次点击"排序"按钮退出排序模式
   - [ ] 排序按钮恢复透明
   - [ ] 复选框重新显示
   - [ ] 新建按钮恢复可用
   - [ ] 显示"排序已保存"提示
5. 关闭对话框，重新打开
   - [ ] 分类顺序保持为："分类3"、"分类1"、"分类2"

#### 测试 3: 右键菜单

**步骤**：
1. 右键点击任意分类
   - [ ] 弹出右键菜单
   - [ ] 包含"重命名 (F2)"、"在此新建"、"删除此项"
2. 点击"在此新建"
   - [ ] 弹出输入对话框
   - [ ] 新建的分类作为子分类添加
3. 右键点击子分类，选择"删除此项"
   - [ ] 弹出确认对话框
   - [ ] 仅删除该子分类（不影响其他勾选项）

#### 测试 4: 快捷键

**步骤**：
1. 选中任意分类，按 F2
   - [ ] 触发重命名操作
   - [ ] 弹出输入对话框

#### 测试 5: 帮助提示

**步骤**：
1. 点击"帮助"按钮
   - [ ] 显示 TeachingTip
   - [ ] 内容包含操作指南
   - [ ] 可以关闭

#### 测试 6: 边界条件

**步骤**：
1. 尝试删除系统分类"未分类"
   - [ ] 显示错误提示"系统分类无法删除"
2. 创建 3 层嵌套分类，尝试创建第 4 层
   - [ ] 显示错误提示"分类层级不能超过 3 层"
3. 在排序模式下尝试双击分类
   - [ ] 无任何响应（双击被禁用）

---

## 实施顺序

1. **阶段 1**: 后端增强（新增 `reorder_categories` 和 `rename_category` 方法）
2. **阶段 2**: UI 组件重构（重构工具栏和树形控件）
3. **阶段 3**: 双模式交互逻辑（实现模式切换）
4. **阶段 4**: 基础编辑功能实现（新建、重命名、删除）
5. **阶段 5**: 排序功能实现（拖拽排序、验证逻辑、持久化）⭐ **独立步骤**
6. **阶段 6**: 操作日志功能（日志记录、查看界面）📝 **可选功能**
7. **阶段 7**: 右键菜单和帮助系统
8. **阶段 8**: 手动验证测试

---

## 风险与注意事项

> [!CAUTION]
> **数据安全**
> 
> 由于采用即时保存机制，所有操作无法撤销。建议在实施前：
> 1. 提醒用户备份 `config/categories.json` 文件
> 2. 在删除操作前显示详细的确认对话框
> 3. ✅ **已添加操作日志功能**（阶段 6）- 记录所有分类变更历史

> [!WARNING]
> **性能考虑**
> 
> 如果分类数量超过 100 个，拖拽排序可能出现性能问题。建议：
> 1. 限制分类总数（例如最多 50 个）
> 2. 优化树形控件的渲染性能
> 3. 考虑使用虚拟滚动（如果 QFluentWidgets 支持）
