# 配置系统指南

本文档说明 Ghost-Dir 应用的配置系统架构和使用方法。

## 📁 配置文件职责划分

### `src/common/config.py` - 应用级常量配置
**职责：** 存放应用级的不可变常量

包含内容：
- 应用信息（名称、版本、作者）
- 文件路径配置
- UI 常量（窗口尺寸、颜色、图标）
- **默认值常量**（所有用户配置的初始值）
- **选项配置**（UI 组件的可选项定义）
- 系统黑名单

### `src/data/user_manager.py` - 用户数据管理
**职责：** 管理运行时可变的用户数据

包含内容：
- 加载/保存用户数据到 JSON 文件
- 管理连接、分类、模板
- 提供 getter/setter 方法
- **引用** `config.py` 中的默认值常量

---

## 🎨 主题和颜色配置

### 1. 默认值配置

在 `config.py` 中定义默认值：

```python
# 主题默认值
DEFAULT_THEME = "system"  # 可选值: "light", "dark", "system"
DEFAULT_THEME_COLOR = "system"  # 可选值: "system" 或 十六进制颜色值如 "#009FAA"

# 启动页默认值
DEFAULT_STARTUP_PAGE = "wizard"  # 可选值: "wizard", "console", "library"
```

### 2. 选项配置

在 `config.py` 中定义可选项列表：

```python
# 主题模式选项
THEME_OPTIONS = [
    {"value": "system", "i18n_key": "settings.theme_system"},
    {"value": "light", "i18n_key": "settings.theme_light"},
    {"value": "dark", "i18n_key": "settings.theme_dark"},
]

# 主题色选项
THEME_COLOR_OPTIONS = [
    {"value": "system", "i18n_key": "settings.theme_color_system"},
    {"value": "#009FAA", "i18n_key": "settings.theme_color_teal"},
    {"value": "#0078D4", "i18n_key": "settings.theme_color_blue"},
    # ... 更多颜色
]

# 启动页选项
STARTUP_PAGE_OPTIONS = [
    {"value": "wizard", "i18n_key": "settings.startup_wizard"},
    {"value": "console", "i18n_key": "settings.startup_console"},
    {"value": "library", "i18n_key": "settings.startup_library"},
]
```

### 3. UI 组件使用

在设置卡片组件中使用配置：

```python
from .....common.config import THEME_COLOR_OPTIONS, DEFAULT_THEME_COLOR
from ....i18n import t

class ThemeColorCard(ComboBoxSettingCard):
    def __init__(self, user_manager, parent=None):
        # 从配置构建颜色映射字典
        self.color_map = {
            t(option["i18n_key"]): option["value"]
            for option in THEME_COLOR_OPTIONS
        }
        
        # 使用默认值
        config_item = OptionsConfigItem(
            "Appearance", "ThemeColor", DEFAULT_THEME_COLOR,
            OptionsValidator(list(self.color_map.values())),
        )
```

---

## ✨ 配置系统优势

### 1. **单一数据源**
所有默认值和选项都在 `config.py` 中定义，消除了硬编码

### 2. **灵活可配置**
要添加新的主题色，只需在 `THEME_COLOR_OPTIONS` 中添加一项：

```python
THEME_COLOR_OPTIONS = [
    # ... 现有选项
    {"value": "#FF6B6B", "i18n_key": "settings.theme_color_pink"},  # 新增粉色
]
```

### 3. **国际化友好**
所有显示文本通过 `i18n_key` 引用，支持多语言

### 4. **易于维护**
- 修改默认主题色：只需修改 `DEFAULT_THEME_COLOR`
- 添加新选项：只需在对应的 `OPTIONS` 列表中添加
- 调整选项顺序：直接调整列表顺序即可

---

## 🔧 如何添加新的配置选项

### 步骤 1: 在 `config.py` 中定义

```python
# 默认值
DEFAULT_MY_SETTING = "option1"

# 选项列表
MY_SETTING_OPTIONS = [
    {"value": "option1", "i18n_key": "settings.my_setting_option1"},
    {"value": "option2", "i18n_key": "settings.my_setting_option2"},
]
```

### 步骤 2: 在 `user_manager.py` 中添加管理方法

```python
from ..common.config import DEFAULT_MY_SETTING

class UserManager:
    def __init__(self):
        self.my_setting: str = DEFAULT_MY_SETTING
        
    def set_my_setting(self, value: str) -> bool:
        try:
            self.my_setting = value
            self._save_data()
            return True
        except Exception as e:
            print(f"设置失败: {e}")
            return False
    
    def get_my_setting(self) -> str:
        return self.my_setting
```

### 步骤 3: 创建 UI 组件

```python
from .....common.config import MY_SETTING_OPTIONS, DEFAULT_MY_SETTING

class MySettingCard(ComboBoxSettingCard):
    def __init__(self, user_manager, parent=None):
        self.setting_map = {
            t(option["i18n_key"]): option["value"]
            for option in MY_SETTING_OPTIONS
        }
        # ... 其余实现
```

---

## 📝 注意事项

1. **不要在组件中硬编码选项**  
   ❌ 错误：`self.options = ["选项1", "选项2"]`  
   ✅ 正确：从 `config.py` 导入 `OPTIONS` 配置

2. **使用默认值常量**  
   ❌ 错误：`data.get('theme', 'system')`  
   ✅ 正确：`data.get('theme', DEFAULT_THEME)`

3. **保持配置集中**  
   所有应用级常量都应在 `config.py` 中定义，避免分散在各个文件中

4. **国际化键命名规范**  
   使用点分隔的命名：`"settings.theme_color_blue"`

---

## 🎯 配置文件清单

| 文件 | 职责 | 示例内容 |
|------|------|---------|
| `config.py` | 应用常量 | 默认值、选项列表、UI 常量 |
| `user_manager.py` | 数据管理 | 加载/保存、getter/setter |
| `theme_card.py` | UI 组件 | 使用配置构建界面 |
| `config.json` | 用户数据 | 运行时保存的用户设置 |

---

**最后更新：** 2026-01-26  
**版本：** 7.4.0
