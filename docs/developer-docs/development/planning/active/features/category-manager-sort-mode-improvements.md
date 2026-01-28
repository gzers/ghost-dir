# 排序模式改进说明

## 改进内容

### 1. 使用 TogglePushButton

**之前**：使用普通的 `PushButton` + `setCheckable(True)`
```python
self.sortButton = PushButton(FluentIcon.SYNC, "排序")
self.sortButton.setCheckable(True)
```

**现在**：使用专门的 `TogglePushButton`
```python
from qfluentwidgets import TogglePushButton
self.sortButton = TogglePushButton("排序")
self.sortButton.setIcon(FluentIcon.SYNC)
```

**优势**：
- TogglePushButton 有更明显的按下/未按下视觉状态
- 按下时背景色会改变，更容易识别当前状态

### 2. 动态按钮文本

**浏览模式**：
- 按钮文本：`"排序"`
- 标题：`"分类管理"`

**排序模式**：
- 按钮文本：`"退出排序"`
- 标题：`"分类管理 - 排序模式"`

**代码实现**：
```python
def _enter_sort_mode(self):
    self.titleLabel.setText("分类管理 - 排序模式")
    self.sortButton.setText("退出排序")
    # ...

def _enter_browse_mode(self):
    self.titleLabel.setText("分类管理")
    self.sortButton.setText("排序")
    # ...
```

### 3. 禁用对话框按钮

**排序模式下**：
- 禁用"完成"按钮 (`yesButton`)
- 禁用"取消"按钮 (`cancelButton`)

**原因**：
- 防止用户在排序模式下意外关闭对话框
- 强制用户必须先退出排序模式才能关闭对话框
- 确保排序操作的完整性

**代码实现**：
```python
def _enter_sort_mode(self):
    # 禁用对话框按钮（防止在排序模式下关闭）
    self.yesButton.setEnabled(False)
    self.cancelButton.setEnabled(False)
    # ...

def _enter_browse_mode(self):
    # 恢复对话框按钮
    self.yesButton.setEnabled(True)
    self.cancelButton.setEnabled(True)
    # ...
```

## 用户体验改进

### 视觉反馈

1. **按钮状态更明显**
   - TogglePushButton 在按下时有明显的背景色变化
   - 按钮文本从"排序"变为"退出排序"

2. **标题栏提示**
   - 标题从"分类管理"变为"分类管理 - 排序模式"
   - 用户始终知道当前处于什么模式

3. **按钮禁用状态**
   - 排序模式下，所有编辑按钮（新建、重命名、删除）被禁用
   - 对话框按钮（完成、取消）也被禁用
   - 只有"退出排序"按钮和"帮助"按钮可用

### 操作流程

**进入排序模式**：
1. 点击"排序"按钮
2. 按钮变为"退出排序"，背景高亮
3. 标题变为"分类管理 - 排序模式"
4. 所有其他按钮被禁用
5. 复选框消失
6. 可以拖拽分类调整顺序

**退出排序模式**：
1. 点击"退出排序"按钮
2. 自动保存排序
3. 按钮恢复为"排序"，背景恢复正常
4. 标题恢复为"分类管理"
5. 所有按钮恢复可用
6. 复选框重新显示

## 测试要点

- [ ] 排序按钮的视觉状态明显（按下时背景色改变）
- [ ] 按钮文本正确切换（"排序" ↔ "退出排序"）
- [ ] 标题正确切换（"分类管理" ↔ "分类管理 - 排序模式"）
- [ ] 排序模式下无法点击"完成"或"取消"按钮
- [ ] 排序模式下无法使用新建、重命名、删除功能
- [ ] 退出排序模式后所有功能恢复正常
