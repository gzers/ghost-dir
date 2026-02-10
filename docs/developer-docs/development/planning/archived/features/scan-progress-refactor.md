# 扫描进度组件重构说明

- 适用版本: `历史归档`
- 文档状态: `archived`
- 最后更新: `2026-02-10`

## 概述

本次重构对 `scan_progress.py` 进行了全面的组件化改造，消除了硬编码，采用了统一的样式系统和国际化方案。

## 主要改进

### 1. 组件化设计

#### 新增可复用组件

**CardHeader 组件** (`src/gui/components/card_header.py`)
- 封装了卡片头部的图标、标题和副标题显示逻辑
- 使用统一的样式系统进行排版
- 可在其他卡片组件中复用

**ProgressIndicator 组件** (`src/gui/components/progress_indicator.py`)
- 封装了进度条和状态文本的显示逻辑
- 提供了清晰的 API：
  - `start_indeterminate()` - 开始不确定进度
  - `set_progress(current, total)` - 设置确定进度
  - `set_status(text)` - 设置状态文本
  - `complete()` - 完成进度
  - `hide_progress()` - 隐藏进度条
  - `reset()` - 重置状态

#### 重构后的组件结构

```
ScanProgressCard (主组件)
├── CardHeader (卡片头部)
│   ├── Icon (图标)
│   ├── Title (标题)
│   └── Subtitle (副标题)
├── ProgressIndicator (进度指示器)
│   ├── ProgressBar (进度条)
│   └── StatusLabel (状态文本)
├── ResultLabel (结果统计)
└── ButtonGroup (按钮组)
    ├── ScanButton (扫描按钮)
    ├── ImportButton (导入按钮)
    ├── RefreshButton (刷新按钮)
    └── CancelButton (取消按钮)
```

### 2. 消除硬编码

#### 样式系统集成

**之前（硬编码）：**
```python
self.main_layout.setContentsMargins(24, 24, 24, 24)
self.main_layout.setSpacing(16)
self.icon_label.setFixedSize(40, 40)
```

**之后（使用样式系统）：**
```python
self.main_layout.setContentsMargins(
    get_spacing("lg"),
    get_spacing("lg"),
    get_spacing("lg"),
    get_spacing("lg")
)
self.main_layout.setSpacing(get_spacing("md"))
# 图标大小由 apply_icon_style 统一管理
```

#### 国际化 (i18n)

**之前（硬编码文案）：**
```python
self.title_label = StrongBodyLabel("智能扫描")
self.status_label = BodyLabel("自动发现本机可管理的软件")
self.scan_button = PrimaryPushButton(FluentIcon.SEARCH, "开始扫描")
self.detail_label.setText("点击扫描开始")
self.detail_label.setText(f"正在扫描: {current}/{total}")
```

**之后（使用 i18n）：**
```python
self.header = CardHeader(
    icon=t("wizard.scan_card_icon"),
    title=t("wizard.scan_card_title"),
    subtitle=t("wizard.scan_card_subtitle")
)
self.scan_button = PrimaryPushButton(
    FluentIcon.SEARCH,
    t("wizard.start_scan")
)
self.progress_indicator.set_status(t("wizard.scan_idle"))
self.progress_indicator.set_status(
    t("wizard.scan_progress_count", current=current, total=total)
)
```

### 3. 代码质量提升

#### 类型注解
所有方法参数和返回值都添加了类型注解：
```python
def update_progress(self, current: int, total: int):
def scan_finished(self, discovered_count: int, selected_count: int):
def set_import_enabled(self, enabled: bool):
```

#### 文档字符串
为所有公共方法添加了详细的文档字符串：
```python
def update_progress(self, current: int, total: int):
    """
    更新进度
    
    Args:
        current: 当前进度
        total: 总进度
    """
```

#### 代码组织
- 将按钮初始化逻辑提取到独立方法 `_init_buttons()`
- 移除了冗余的 `_refresh_content_styles()` 方法
- 使用组件封装减少了主类的复杂度

### 4. 新增功能

#### update_selected_count 方法
```python
def update_selected_count(self, count: int):
    """
    更新选中数量
    
    Args:
        count: 选中数量
    """
    self.selected_count = count
    if self.result_label.isVisible():
        self.result_label.setText(
            t("wizard.selected_count", count=count)
        )
    # 更新导入按钮状态
    self.set_import_enabled(count > 0)
```

这个方法允许外部组件动态更新选中数量，并自动同步 UI 状态。

## 文件变更清单

### 新增文件
1. `src/gui/components/card_header.py` - 卡片头部组件
2. `src/gui/components/progress_indicator.py` - 进度指示器组件

### 修改文件
1. `src/gui/components/__init__.py` - 导出新组件
2. `src/gui/i18n/zh_CN/wizard.py` - 添加扫描相关文案
3. `src/gui/views/wizard/widgets/scan_progress.py` - 主要重构文件

## 使用示例

```python
# 创建扫描进度卡片
scan_card = ScanProgressCard()

# 连接信号
scan_card.scan_clicked.connect(on_scan)
scan_card.import_clicked.connect(on_import)

# 开始扫描
scan_card.start_scanning()

# 更新进度
scan_card.update_progress(current=5, total=10)

# 扫描完成
scan_card.scan_finished(discovered_count=10, selected_count=8)

# 动态更新选中数量
scan_card.update_selected_count(5)

# 扫描出错
scan_card.scan_error("网络连接失败")

# 重置状态
scan_card.reset()
```

## 优势总结

1. **可维护性** - 组件化设计使代码更易理解和维护
2. **可复用性** - CardHeader 和 ProgressIndicator 可在其他地方使用
3. **一致性** - 使用统一的样式系统确保 UI 一致性
4. **国际化** - 所有文案集中管理，易于翻译
5. **类型安全** - 完整的类型注解减少运行时错误
6. **文档完善** - 详细的文档字符串提高代码可读性
7. **灵活性** - 新增的 `update_selected_count` 方法提供更好的状态管理

## 后续建议

1. 考虑为其他卡片组件应用相同的重构模式
2. 可以进一步提取 ButtonGroup 为独立组件
3. 考虑添加单元测试覆盖新组件
4. 可以为 ProgressIndicator 添加动画效果配置
