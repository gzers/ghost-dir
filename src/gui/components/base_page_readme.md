# BasePageView 使用说明

## 概述

`BasePageView` 是一个页面视图基类，用于统一所有窗口页面的布局结构，减少重复代码。

## 公共部分抽象

### 原有代码结构（重构前）

每个视图文件都有相似的代码：

```python
def _init_ui(self):
    layout = QVBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # 标题
    title_layout = QHBoxLayout()
    from ...styles import apply_page_layout
    apply_page_layout(title_layout, spacing="section")
    title_layout.setContentsMargins(24, 24, 24, 8)
    from qfluentwidgets import TitleLabel
    self.title_label = TitleLabel(t("xxx.title"))
    title_layout.addWidget(self.title_label)
    title_layout.addStretch()  # 右侧工具栏占位
    layout.addLayout(title_layout)

    # 滚动区域
    self.scroll = ScrollArea()
    self.scroll.setWidgetResizable(True)
    self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    self.container = QWidget()
    self.container_layout = QVBoxLayout(self.container)
    apply_page_layout(self.container_layout, spacing="group")
    self.container_layout.setContentsMargins(24, 12, 24, 24)
    self.container_layout.addStretch()

    self.scroll.setWidget(self.container)
    layout.addWidget(self.scroll)

    # 主题样式处理
    self._update_theme_style()
    from ....common.signals import signal_bus
    signal_bus.theme_changed.connect(self._on_theme_changed)

def _update_theme_style(self):
    from ...styles import apply_container_style
    apply_container_style(self.container)

def _on_theme_changed(self, theme):
    self._update_theme_style()
```

### 重构后（使用 BasePageView）

```python
class MyView(BasePageView):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("myview.title"),
            show_toolbar=False,  # 可选：是否显示工具栏
            enable_scroll=True   # 可选：是否启用滚动
        )

        # 直接添加内容，无需关心布局和主题
        self._setup_content()

    def _setup_content(self):
        # 使用 add_to_content 添加控件
        card = MyCard()
        self.add_to_content(card)
```

## 特性

### 1. 统一布局规范

- 标题区域：包含标题标签和可选的右侧工具栏
- 工具栏区域：可选的搜索、筛选等控件区域
- 内容区域：支持滚动或固定布局
- 自动应用间距和边距规范

### 2. 支持两种布局模式

| 模式 | 布局类型 | 适用场景 | 标题栏 |
|------|---------|---------|--------|
| 普通 | QVBoxLayout | 一般页面 | 有 |
| Expand | ExpandLayout | 设置页面 | 无（内部添加） |

**ExpandLayout 模式**：
- 使用 QFluentWidgets 的 `ExpandLayout`
- 滚动区域背景透明
- 容器使用 `apply_page_style` 而非 `apply_container_style`
- 适合设置卡片组等折叠展开内容

### 3. 简化的 API

| 功能 | 原有方式 | 使用 BasePageView |
|------|---------|------------------|
| 添加内容 | `container_layout.addWidget(widget)` | `add_to_content(widget)` |
| 添加右侧工具 | `title_layout.addWidget(widget)` | `get_right_toolbar_layout().addWidget(widget)` |
| 获取滚动区域 | 直接访问 `self.scroll` | `get_scroll_area()` |
| 清空内容 | 手动循环删除 | `clear_content()` |
| 设置标题 | `self.title_label.setText(text)` | `set_title(text)` |

### 4. 自动主题处理

- 自动监听 `signal_bus.theme_changed` 信号
- 自动更新容器背景样式
- 滚动区域背景透明
- 子类可通过重写 `_on_theme_changed` 添加额外逻辑

## API 文档

### 构造函数参数

```python
BasePageView(
    parent=None,           # 父组件
    title: str = "",       # 页面标题
    show_toolbar: bool = False,  # 是否显示工具栏区域
    enable_scroll: bool = True,  # 是否启用滚动区域
    use_expand_layout: bool = False  # 是否使用 ExpandLayout
)
```

**参数说明**：
- `use_expand_layout=True` 时：
  - 标题栏不自动创建（可在内容区域内手动添加）
  - 使用 `ExpandLayout` 作为内容布局
  - 滚动区域背景透明
  - 容器应用 `apply_page_style`

### 公共方法

#### `set_title(title: str)`
设置页面标题。

#### `get_title_label() -> TitleLabel`
获取标题标签组件（ExpandLayout 模式下为 None）。

#### `get_right_toolbar_layout() -> QHBoxLayout`
获取右侧工具栏布局，用于在标题栏右侧添加控件。

```python
# 示例：添加刷新按钮
toolbar = self.get_right_toolbar_layout()
refresh_btn = PushButton("刷新", icon=FluentIcon.SYNC)
toolbar.addWidget(refresh_btn)
```

#### `get_toolbar_layout() -> QHBoxLayout`
获取工具栏区域布局，用于添加搜索、筛选等控件。

```python
# 示例：添加搜索框
toolbar = self.get_toolbar_layout()
search = SearchLineEdit()
search.setPlaceholderText("搜索...")
toolbar.addWidget(search)
```

#### `get_content_layout()`
获取内容区域布局（`QVBoxLayout` 或 `ExpandLayout`）。

#### `get_scroll_area() -> ScrollArea`
获取滚动区域组件（未启用滚动时返回 None）。

#### `get_content_container() -> QWidget`
获取内容容器组件。

#### `add_to_content(widget: QWidget, before_stretch: bool = True)`
添加控件到内容区域。

- `before_stretch=True`: 插入到底部 stretch 之前（仅 QVBoxLayout 模式有效）
- `before_stretch=False`: 添加到布局末尾

```python
# 普通模式（推荐）
self.add_to_content(my_card)

# ExpandLayout 模式（直接添加）
self.add_to_content(my_card)
```

#### `clear_content()`
清空内容区域的所有控件。

```python
# 示例：刷新数据
self.clear_content()
for item in new_data:
    card = create_card(item)
    self.add_to_content(card)
```

#### `show_empty_state(message: str = "暂无内容")`
显示空状态提示。

```python
# 示例：无数据时显示空状态
if not data:
    self.show_empty_state("暂无可用模板")
```

## 重构示例

### WizardView 重构前后对比

| 指标 | 重构前 | 重构后 | 变化 |
|------|--------|--------|------|
| 总代码行数 | 240 | 207 | -14% |
| 布局代码行数 | ~60 | ~10 | -83% |
| 重复的样式代码 | 3 处 | 0 处 | -100% |

### LibraryView 使用建议

```python
class LibraryView(BasePageView):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title=t("library.title"),
            show_toolbar=True,   # 启用工具栏
            enable_scroll=True
        )

        # 添加搜索和筛选到工具栏
        toolbar = self.get_toolbar_layout()
        self.search_edit = SearchLineEdit()
        self.search_edit.setPlaceholderText(t("library.search_placeholder"))
        self.search_edit.setFixedWidth(300)
        toolbar.addWidget(self.search_edit)

        # 添加右侧统计按钮
        right_toolbar = self.get_right_toolbar_layout()
        self.count_label = PushButton()
        self.count_label.setEnabled(False)
        right_toolbar.addWidget(self.count_label)
```

### SettingView 使用 ExpandLayout

```python
class SettingView(BasePageView):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title="",  # ExpandLayout 模式下不使用外部标题
            show_toolbar=False,
            enable_scroll=True,
            use_expand_layout=True  # 启用 ExpandLayout
        )
        self._setup_content()

    def _setup_content(self):
        # 获取 ExpandLayout
        expand_layout = self.get_content_layout()

        # 在内容区域内手动添加标题
        title_label = TitleLabel(t("settings.title"), self.get_content_container())
        expand_layout.addWidget(title_label)

        # 添加设置卡片组
        group = SettingCardGroup("组标题", self.get_content_container())
        card = PushSettingCard(...)
        group.addSettingCard(card)
        expand_layout.addWidget(group)
```

## 主题事件

### `theme_changed` 信号

当主题变更时触发，子类可连接此信号：

```python
self.theme_changed.connect(self._handle_custom_theme_change)

def _handle_custom_theme_change(self, theme):
    # 自定义主题处理逻辑
    pass
```

### 重写 `_on_theme_changed`

```python
def _on_theme_changed(self, theme):
    super()._on_theme_changed(theme)  # 先调用父类方法
    # 添加自定义处理
    self._refresh_card_styles()
```

## 注意事项

1. **设置视图（SettingView）**：使用 `use_expand_layout=True` 模式，标题在内容区域内手动添加。

2. **帮助视图（HelpView）**：内容简单且不需要滚动，可使用 `enable_scroll=False`。

3. **布局操作**：
   - 普通模式：推荐使用 `add_to_content(widget)` 确保正确插入到 stretch 之前
   - ExpandLayout 模式：直接使用 `expand_layout.addWidget(widget)`

4. **主题样式**：
   - 普通模式：使用 `apply_container_style`
   - ExpandLayout 模式：使用 `apply_page_style`
   - 自定义控件仍需自行处理主题样式

5. **滚动区域**：所有启用滚动的页面都会自动设置背景透明。

## 文件位置

- 基类：`src/gui/components/base_page.py`
- 导出：`src/gui/components/__init__.py`
