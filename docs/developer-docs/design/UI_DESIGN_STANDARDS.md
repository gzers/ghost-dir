# UI 设计规范

本文档定义了应用的 UI 设计标准，基于 Windows 11 Fluent Design System。

## 透明度规范

### 弹出窗口和下拉菜单

根据 Windows 11 Fluent Design System 的 Acrylic 材质规范：

#### 标准透明度值

- **弹出窗口（Popup）**: 95% 不透明度 (由于叠加文字预览需求，已从 90% 提升至 95%)
  - 亮色主题: `rgba(255, 255, 255, 0.95)`
  - 暗色主题: `rgba(45, 45, 45, 0.95)`

- **对话框背景（Dialog）**: 95% 不透明度
  - 亮色主题: `rgba(255, 255, 255, 0.95)`
  - 暗色主题: `rgba(45, 45, 45, 0.95)`

- **侧边栏（Sidebar）**: 85% 不透明度
  - 亮色主题: `rgba(249, 249, 249, 0.85)`
  - 暗色主题: `rgba(30, 30, 30, 0.85)`

#### 使用场景

| 组件类型 | 不透明度 | 说明 |
|---------|---------|------|
| 下拉菜单 | 90% | 如分类选择器、ComboBox 下拉列表 |
| 右键菜单 | 90% | 上下文菜单 |
| 工具提示 | 95% | Tooltip |
| 模态对话框 | 95% | MessageBox、编辑对话框 |
| 侧边导航 | 85% | NavigationPanel |

### 实现示例

```python
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette

def get_popup_background():
    """获取弹出窗口的标准背景色"""
    palette = QApplication.palette()
    is_dark = palette.color(QPalette.ColorRole.Window).lightness() < 128
    return "rgba(45, 45, 45, 0.95)" if is_dark else "rgba(255, 255, 255, 0.95)"

def get_dialog_background():
    """获取对话框的标准背景色"""
    palette = QApplication.palette()
    is_dark = palette.color(QPalette.ColorRole.Window).lightness() < 128
    return "rgba(45, 45, 45, 0.95)" if is_dark else "rgba(255, 255, 255, 0.95)"
```

## 交互规范

### 可点击元素

所有可点击的元素应该提供视觉反馈：

1. **鼠标指针**
   - 可点击元素: `Qt.CursorShape.PointingHandCursor`
   - 文本选择: `Qt.CursorShape.IBeamCursor`
   - 拖拽: `Qt.CursorShape.OpenHandCursor`

2. **悬停效果**
   - 背景色变化: `rgba(0, 0, 0, 0.05)` (亮色主题)
   - 背景色变化: `rgba(255, 255, 255, 0.05)` (暗色主题)

### 输入框

#### 只读输入框作为选择器

当输入框用作选择器（如分类选择器）时：

```python
lineEdit.setReadOnly(True)
lineEdit.setCursor(Qt.CursorShape.PointingHandCursor)
lineEdit.mousePressEvent = lambda event: show_selector()
```

**不要**添加额外的下拉按钮，直接点击输入框即可触发。

## 边框规范

### 弹出窗口边框

- **宽度**: 1px
- **颜色**: `rgba(0, 0, 0, 0.15)` (通用)
- **圆角**: 8px

### 输入框边框

- **宽度**: 1px
- **颜色**: `rgba(0, 0, 0, 0.1)` (默认)
- **颜色**: `rgba(0, 0, 0, 0.2)` (悬停)
- **圆角**: 4px

## 阴影规范

### 弹出窗口阴影

```css
box-shadow: 0 8px 16px rgba(0, 0, 0, 0.14);
```

### 对话框阴影

```css
box-shadow: 0 16px 32px rgba(0, 0, 0, 0.18);
```

## 参考资料

- [Microsoft Fluent Design System](https://fluent2.microsoft.design/)
- [Windows 11 Design Principles](https://learn.microsoft.com/en-us/windows/apps/design/)
- [Acrylic Material](https://learn.microsoft.com/en-us/windows/apps/design/style/acrylic)
