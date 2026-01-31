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

## 状态徽章规范 (StatusBadge)

状态徽章用于直观展示连接实体的生命周期状态。

### 1. 视觉配色与语义

| 状态代号 (Code) | 状态名称 | 语义 | 颜色 (Hex/RGBA) | 图标 (Fluent) |
| :--- | :--- | :--- | :--- | :--- |
| `disconnected` | **未连接** | 实体在 C 盘，是个普通文件夹 | `#E74C3C` (20% Opacity BG) | `\uf111` (警告/红) |
| `connected` | **已连接** | 实体在 D 盘且通过 Junction 接通 | `#27AE60` (20% Opacity BG) | `\uf111` (链接/绿) |
| `ready` | **就绪** | 实体在 D 盘，但 C 盘连接点缺失 | `#F39C12` (20% Opacity BG) | `\uf111` (同步/黄) |
| `invalid` | **失效** | 路径配置错误或物理文件丢失 | `#95A5A6` (20% Opacity BG) | `\uf111` (禁用/灰) |

### 2. 布局规范

- **圆角**: 4px
- **内边距**: `4px 8px`
- **层级**: 在列表视图中建议靠右放置，在表格视图中建议居中。

## 文案与国际化规范

为确保系统语言表达的一致性与地道感，所有 UI 组件必须遵循以下规范：

### 1. 强制使用公共 Getter
禁止在业务代码中直接使用字符串拼接或手动构造 `t()` 函数路径。必须使用 `src.gui.i18n` 提供的公共获取函数：
- **分类文案**：使用 `get_category_text(id_or_name)`。
- **状态文案**：使用 `get_status_text(code)`。

### 2. 映射逻辑收口 (优先级标准)
显示文案的获取必须严格遵循以下优先级：
1. **实时配置展示名 (Persistent Config)**：优先从 `categories.json` 中检索用户手动定义的 `name` 字段。
2. **i18n 智能翻译 (Logic Fallback)**：如果 ID 未在配置中持久化（如扫描过程中的临时 ID），则通过 `get_category_text` 进行分段解析。
3. **原始 ID 透明展示 (Safe Fallback)**：作为最后手段。

UI 层只需负责“传入原始 ID”并展示结果，严禁在业务视图中编写任何静态文案转换代码。

## 参考资料

- [Microsoft Fluent Design System](https://fluent2.microsoft.design/)
- [Windows 11 Design Principles](https://learn.microsoft.com/en-us/windows/apps/design/)
- [Acrylic Material](https://learn.microsoft.com/en-us/windows/apps/design/style/acrylic)
