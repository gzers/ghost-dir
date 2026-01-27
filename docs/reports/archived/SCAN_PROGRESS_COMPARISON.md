# 扫描进度组件重构对比

## 代码行数对比

| 指标 | 重构前 | 重构后 | 变化 |
|------|--------|--------|------|
| 总行数 | 225 | 291 (含新组件) | +66 |
| scan_progress.py | 225 | 235 | +10 |
| 硬编码文案数量 | 15+ | 0 | -15+ |
| 硬编码样式数量 | 10+ | 0 | -10+ |
| 可复用组件 | 0 | 2 | +2 |

## 代码质量对比

### 1. 硬编码消除

#### 文案硬编码

**重构前：**
```python
self.title_label = StrongBodyLabel("智能扫描")
self.status_label = BodyLabel("自动发现本机可管理的软件")
self.scan_button = PrimaryPushButton(FluentIcon.SEARCH, "开始扫描")
self.import_button = PrimaryPushButton(FluentIcon.DOWNLOAD, "一键导入")
self.refresh_button = PushButton(FluentIcon.SYNC, "重新扫描")
self.cancel_button = PushButton(FluentIcon.CLOSE, "取消")
self.detail_label.setText("点击扫描开始")
self.detail_label.setText("正在扫描本机，请稍候...")
self.detail_label.setText(f"正在扫描: {current}/{total}")
self.detail_label.setText(f"扫描完成！发现 {discovered_count} 个可管理的软件")
self.result_label.setText(f"已选中 {selected_count} 项")
self.detail_label.setText("未发现可管理的软件")
self.detail_label.setText(f"扫描失败: {error_msg}")
```

**重构后：**
```python
# 所有文案通过 i18n 系统管理
self.header = CardHeader(
    icon=t("wizard.scan_card_icon"),
    title=t("wizard.scan_card_title"),
    subtitle=t("wizard.scan_card_subtitle")
)
self.scan_button = PrimaryPushButton(FluentIcon.SEARCH, t("wizard.start_scan"))
self.import_button = PrimaryPushButton(FluentIcon.DOWNLOAD, t("wizard.import_selected"))
self.refresh_button = PushButton(FluentIcon.SYNC, t("wizard.rescan"))
self.cancel_button = PushButton(FluentIcon.CLOSE, t("wizard.cancel"))
self.progress_indicator.set_status(t("wizard.scan_idle"))
self.progress_indicator.set_status(t("wizard.scan_progress_detail"))
self.progress_indicator.set_status(t("wizard.scan_progress_count", current=current, total=total))
```

#### 样式硬编码

**重构前：**
```python
self.main_layout.setContentsMargins(24, 24, 24, 24)
self.main_layout.setSpacing(16)
title_layout.addSpacing(12)
self.icon_label.setFixedSize(40, 40)
info_layout.setSpacing(4)
```

**重构后：**
```python
self.main_layout.setContentsMargins(
    get_spacing("lg"),
    get_spacing("lg"),
    get_spacing("lg"),
    get_spacing("lg")
)
self.main_layout.setSpacing(get_spacing("md"))
button_layout.setSpacing(get_spacing("sm"))
# 图标大小由样式系统统一管理
```

### 2. 组件化程度

**重构前：**
- 所有 UI 逻辑都在一个类中
- 进度条和状态标签直接嵌入
- 标题区域使用嵌套布局
- 无法复用任何部分

**重构后：**
- 提取 CardHeader 组件（可复用）
- 提取 ProgressIndicator 组件（可复用）
- 主类只负责组合和协调
- 组件可在其他地方使用

### 3. 代码可读性

**重构前：**
```python
def _init_ui(self):
    """初始化 UI"""
    # 60+ 行代码混在一起
    # 包含布局、样式、事件绑定等
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setContentsMargins(24, 24, 24, 24)
    # ... 大量代码 ...
    
    title_layout = QHBoxLayout()
    self.icon_label = BodyLabel("🔍")
    self.icon_label.setFixedSize(40, 40)
    # ... 更多代码 ...
    
    self.progress_bar = ProgressBar()
    self.progress_bar.setRange(0, 0)
    # ... 继续 ...
```

**重构后：**
```python
def _init_ui(self):
    """初始化 UI"""
    # 清晰的结构，每个部分都是独立组件
    self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
    
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setContentsMargins(...)
    self.main_layout.setSpacing(get_spacing("md"))
    
    # 卡片头部 - 使用组件
    self.header = CardHeader(...)
    self.main_layout.addWidget(self.header)
    
    # 进度指示器 - 使用组件
    self.progress_indicator = ProgressIndicator()
    self.main_layout.addWidget(self.progress_indicator)
    
    # 按钮区域 - 提取到独立方法
    self._init_buttons()
```

### 4. 类型安全

**重构前：**
```python
def update_progress(self, current, total):
    """更新进度"""
    
def scan_finished(self, discovered_count, selected_count):
    """扫描完成"""
    
def scan_error(self, error_msg):
    """扫描出错"""
```

**重构后：**
```python
def update_progress(self, current: int, total: int):
    """
    更新进度
    
    Args:
        current: 当前进度
        total: 总进度
    """
    
def scan_finished(self, discovered_count: int, selected_count: int):
    """
    扫描完成
    
    Args:
        discovered_count: 发现的软件数量
        selected_count: 选中的软件数量
    """
    
def scan_error(self, error_msg: str):
    """
    扫描出错
    
    Args:
        error_msg: 错误信息
    """
```

## 架构改进

### 重构前的架构
```
ScanProgressCard (单体组件)
├── 直接管理所有 UI 元素
├── 硬编码所有文案
├── 硬编码所有样式
└── 无法复用任何部分
```

### 重构后的架构
```
ScanProgressCard (协调器)
├── CardHeader (可复用组件)
│   └── 使用样式系统
├── ProgressIndicator (可复用组件)
│   └── 使用样式系统
├── ResultLabel
│   └── 使用样式系统
└── ButtonGroup
    └── 使用 i18n 系统
```

## 维护性提升

### 修改文案
**重构前：** 需要在代码中查找并修改每个硬编码字符串  
**重构后：** 只需修改 `i18n/zh_CN/wizard.py` 文件

### 修改样式
**重构前：** 需要在代码中查找并修改每个硬编码数值  
**重构后：** 只需修改样式系统的配置

### 添加新语言
**重构前：** 几乎不可能  
**重构后：** 只需添加新的语言文件

### 复用组件
**重构前：** 需要复制粘贴代码  
**重构后：** 直接导入并使用 `CardHeader` 或 `ProgressIndicator`

## 总结

这次重构显著提升了代码质量：

✅ **消除了所有硬编码**  
✅ **提高了组件化程度**  
✅ **增强了代码可读性**  
✅ **改善了类型安全**  
✅ **提升了可维护性**  
✅ **增加了可复用性**  
✅ **支持国际化**  
✅ **遵循统一的设计规范**
