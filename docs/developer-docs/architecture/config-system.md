# 配置系统架构规范

> **版本**: v2.0  
> **最后更新**: 2026-02-06  
> **状态**: 规划中

## 📋 目录

- [核心设计理念](#核心设计理念)
- [配置文件结构](#配置文件结构)
- [配置文件清单](#配置文件清单)
- [核心功能](#核心功能)
- [代码实现规范](#代码实现规范)
- [UI 设计规范](#ui-设计规范)
- [待讨论问题](#待讨论问题)

---

## 核心设计理念

### 官方与用户配置分离

**设计原则**:
- **官方配置**: 只读模板，打包在 `_internal/config`，用户无法修改，可随时恢复
- **用户配置**: 可增删改，存储在 `.ghost-dir`
  - 首次运行时自动从官方配置复制
  - 用户可在设置页面手动触发恢复（需二次确认）⚠️

**优势**:
- ✅ 用户可以自由修改配置，不用担心破坏系统
- ✅ 随时可以恢复到官方默认状态
- ✅ 官方更新时可以选择合并或覆盖
- ✅ 支持配置备份和还原

---

## 配置文件结构

### 开发环境

```
项目根目录/
├── src/
│   ├── main.py
│   ├── common/
│   │   └── config.py                # 配置路径定义
│   └── ...
│
├── config/                          # 官方配置模板（开发环境）
│   ├── default_config.json          # 官方UI配置模板
│   ├── default_categories.json      # 官方分类定义
│   └── default_templates.json       # 官方模板定义
│
├── assets/                          # 资源文件
│   ├── icon.ico
│   └── ...
│
├── .ghost-dir/                      # 运行时数据目录（开发环境）
│   ├── user_config.json             # 用户UI配置
│   ├── categories.json              # 用户分类（可修改）
│   ├── templates.json               # 用户模板（可修改）
│   ├── links.json                   # 用户链接数据
│   ├── backups/                     # 备份目录
│   └── logs/                        # 日志目录
│
├── Ghost-Dir.spec                   # PyInstaller 打包配置
└── README.md
```

**特点**:
- `config/` 目录与 `src/` 平级，存放官方配置模板
- `.ghost-dir/` 在项目根目录下，首次运行时从 `config/` 复制
- `PROJECT_ROOT` 指向项目根目录

### 打包环境

```
打包后/
├── Ghost-Dir.exe
│
├── _internal/                       # PyInstaller 打包资源（只读）
│   ├── config/                      # 官方配置模板（只读）✨
│   │   ├── default_config.json      # 官方UI配置
│   │   ├── default_categories.json  # 官方分类定义
│   │   └── default_templates.json   # 官方模板定义
│   ├── assets/                      # 其他资源
│   │   ├── icon.ico
│   │   └── ...
│   └── ...                          # Python 运行时等
│
└── .ghost-dir/                      # 用户数据目录（可读写）
    ├── user_config.json             # 用户UI配置
    ├── categories.json              # 用户分类（可修改）
    ├── templates.json               # 用户模板（可修改）
    ├── links.json                   # 用户链接数据
    ├── backups/                     # 备份目录
    └── logs/                        # 日志目录
```

**特点**:
- `config/` 被打包到 `_internal/config/`（只读）
- `.ghost-dir/` 在 exe 同级目录，首次运行时从 `_internal/config/` 复制
- `PROJECT_ROOT` 指向 `_internal/` 目录

---

## 配置文件清单

| 文件名 | 位置 | 用途 | 可修改 | 可恢复 |
|--------|------|------|--------|--------|
| `default_config.json` | `_internal/config/` | 官方UI配置模板 | ❌ | - |
| `default_categories.json` | `_internal/config/` | 官方分类定义 | ❌ | - |
| `default_templates.json` | `_internal/config/` | 官方模板定义 | ❌ | - |
| `user_config.json` | `.ghost-dir/` | 用户UI配置 | ✅ | ✅ |
| `categories.json` | `.ghost-dir/` | 用户分类 | ✅ | ✅ |
| `templates.json` | `.ghost-dir/` | 用户模板 | ✅ | ✅ |
| `links.json` | `.ghost-dir/` | 用户链接数据 | ✅ | ❌ |

---

## 核心功能

### 1. 初始化逻辑（首次运行）

```python
# 伪代码
if 首次运行:
    从 _internal/config/default_*.json 复制到 .ghost-dir/
    重命名为用户配置文件:
        default_config.json → user_config.json
        default_categories.json → categories.json
        default_templates.json → templates.json
```

### 2. 恢复默认功能

用户可以在UI中选择恢复：

#### 选项1：恢复所有配置

```python
复制 _internal/config/default_*.json → .ghost-dir/
覆盖 user_config.json, categories.json, templates.json
保留 links.json（用户数据不受影响）
```

#### 选项2：单独恢复

- 恢复默认分类：`default_categories.json` → `categories.json`
- 恢复默认模板：`default_templates.json` → `templates.json`
- 恢复默认UI配置：`default_config.json` → `user_config.json`

### 3. 合并模式（可选）

用户可以选择"合并官方更新"而非完全覆盖：
- 保留用户自定义的分类/模板
- 仅添加官方新增的分类/模板
- 更新官方已有项的属性

---

## 代码实现规范

### 配置路径常量定义

**文件**: `src/common/config.py`

```python
# 官方配置（只读，打包在 _internal/config）
DEFAULT_CONFIG_FILE = PROJECT_ROOT / "config" / "default_config.json"
DEFAULT_CATEGORIES_FILE = PROJECT_ROOT / "config" / "default_categories.json"
DEFAULT_TEMPLATES_FILE = PROJECT_ROOT / "config" / "default_templates.json"

# 用户配置（可读写，存储在 .ghost-dir）
USER_CONFIG_FILE = DATA_DIR / "user_config.json"
USER_CATEGORIES_FILE = DATA_DIR / "categories.json"
USER_TEMPLATES_FILE = DATA_DIR / "templates.json"
USER_LINKS_FILE = DATA_DIR / "links.json"
```

### 打包后初始化逻辑

```python
if getattr(sys, 'frozen', False):
    import shutil
    
    # 配置文件映射：官方 → 用户
    config_mapping = {
        "default_config.json": "user_config.json",
        "default_categories.json": "categories.json",
        "default_templates.json": "templates.json"
    }
    
    for default_name, user_name in config_mapping.items():
        default_file = PROJECT_ROOT / "config" / default_name
        user_file = DATA_DIR / user_name
        
        # 首次运行：复制官方配置到用户目录
        if not user_file.exists() and default_file.exists():
            shutil.copy2(default_file, user_file)
    
    # 兼容旧版本：自动迁移
    _migrate_old_configs()
```

### 配置恢复服务

**文件**: `src/core/services/config_restore_service.py`

```python
class ConfigRestoreService:
    """配置恢复服务"""
    
    def restore_all_defaults(self) -> Tuple[bool, str]:
        """恢复所有默认配置（不影响links.json）"""
        
    def restore_categories(self) -> Tuple[bool, str]:
        """仅恢复默认分类"""
        
    def restore_templates(self) -> Tuple[bool, str]:
        """仅恢复默认模板"""
        
    def restore_ui_config(self) -> Tuple[bool, str]:
        """仅恢复默认UI配置"""
        
    def merge_official_updates(self, target: str) -> Tuple[bool, str]:
        """合并官方更新（保留用户自定义）"""
```

### PyInstaller 打包配置

**文件**: `Ghost-Dir.spec`

```python
datas=[
    ('assets', 'assets'),              # 资源文件
    ('config', 'config'),              # 官方配置模板 ✨ 关键
],
```

**打包结果映射**:

| 打包前（源码） | 打包后（dist） | 说明 |
|---------------|---------------|------|
| `config/default_config.json` | `_internal/config/default_config.json` | 官方UI配置 |
| `config/default_categories.json` | `_internal/config/default_categories.json` | 官方分类 |
| `config/default_templates.json` | `_internal/config/default_templates.json` | 官方模板 |

---

## UI 设计规范

### 设置页面 - 配置管理功能区

在设置页面添加"配置管理"分组：

```
┌─────────────────────────────────────────┐
│  ⚙️ 配置管理                            │
├─────────────────────────────────────────┤
│                                         │
│  🔄 恢复默认配置                        │
│  ├─ 恢复所有默认配置         [恢复]    │
│  ├─ 恢复默认分类             [恢复]    │
│  ├─ 恢复默认模板             [恢复]    │
│  └─ 恢复默认UI配置           [恢复]    │
│                                         │
│  💾 备份与还原                          │
│  ├─ 导出配置备份             [导出]    │
│  └─ 从备份还原               [还原]    │
│                                         │
└─────────────────────────────────────────┘
```

### 交互流程

#### 恢复所有默认配置

```
第一步：显示警告对话框
┌─────────────────────────────────────┐
│  ⚠️  警告                           │
├─────────────────────────────────────┤
│  此操作将：                         │
│  • 恢复默认UI配置                   │
│  • 恢复默认分类定义                 │
│  • 恢复默认模板定义                 │
│                                     │
│  您的自定义配置将被覆盖！           │
│  （用户链接数据不受影响）           │
│                                     │
│  是否继续？                         │
│                                     │
│     [取消]         [确认恢复]       │
└─────────────────────────────────────┘

第二步：执行恢复操作
- 显示进度提示："正在恢复默认配置..."
- 调用 ConfigRestoreService.restore_all_defaults()
- 重新加载配置
- 刷新UI

第三步：显示成功提示
┌─────────────────────────────────────┐
│  ✅  成功                           │
├─────────────────────────────────────┤
│  默认配置已恢复！                   │
│  应用将重新加载配置。               │
│                                     │
│            [确定]                   │
└─────────────────────────────────────┘
```

#### 单独恢复

```
警告对话框（简化版）
┌─────────────────────────────────────┐
│  ⚠️  确认恢复默认分类               │
├─────────────────────────────────────┤
│  此操作将覆盖您的自定义分类！       │
│  （已创建的链接不受影响）           │
│                                     │
│  是否继续？                         │
│                                     │
│     [取消]         [确认]           │
└─────────────────────────────────────┘
```

### 代码实现示例

```python
class SettingInterface(ScrollArea):
    def __init__(self):
        # ... 现有代码 ...
        
        # 配置管理分组
        self.configGroup = SettingCardGroup("配置管理", self.scrollWidget)
        
        # 恢复所有默认配置
        self.restoreAllCard = PushSettingCard(
            "恢复",
            FluentIcon.SYNC,
            "恢复所有默认配置",
            "将分类、模板和UI配置恢复为官方默认值（不影响链接数据）",
            self.configGroup
        )
        self.restoreAllCard.clicked.connect(self._on_restore_all_clicked)
        
        # 恢复默认分类
        self.restoreCategoriesCard = PushSettingCard(
            "恢复",
            FluentIcon.TAG,
            "恢复默认分类",
            "恢复官方分类定义",
            self.configGroup
        )
        self.restoreCategoriesCard.clicked.connect(self._on_restore_categories_clicked)
        
        # ... 其他恢复按钮 ...
    
    def _on_restore_all_clicked(self):
        """恢复所有默认配置"""
        # 显示警告对话框
        title = "警告"
        content = (
            "此操作将：\n"
            "• 恢复默认UI配置\n"
            "• 恢复默认分类定义\n"
            "• 恢复默认模板定义\n\n"
            "您的自定义配置将被覆盖！\n"
            "(用户链接数据不受影响)\n\n"
            "是否继续？"
        )
        
        dialog = MessageBox(title, content, self.window())
        dialog.yesButton.setText("确认恢复")
        dialog.cancelButton.setText("取消")
        
        if dialog.exec():
            # 用户确认，执行恢复
            self._execute_restore_all()
    
    def _execute_restore_all(self):
        """执行恢复操作"""
        from src.core.services.context import service_bus
        
        # 显示加载提示
        StateTooltip.create(
            target=self.restoreAllCard,
            title="正在恢复默认配置...",
            content="",
            parent=self
        )
        
        # 调用服务
        success, msg = service_bus.config_restore_service.restore_all_defaults()
        
        if success:
            # 成功提示
            InfoBar.success(
                title="恢复成功",
                content="默认配置已恢复，应用将重新加载配置",
                parent=self
            )
            # 重新加载配置
            self._reload_all_configs()
        else:
            # 失败提示
            InfoBar.error(
                title="恢复失败",
                content=msg,
                parent=self
            )
```

### UI 设计关键点

- ⚠️ 所有恢复操作都必须有**二次确认**对话框
- 📝 警告信息要**明确说明**哪些数据会被覆盖，哪些不受影响
- 🔄 恢复后要**自动重新加载**配置并刷新UI
- 💾 建议在恢复前**自动创建备份**（可选功能）

---

## 待讨论问题

### Q1: 用户修改后，如何区分"用户自定义"和"官方项"？

**方案A**: 在数据结构中添加 `source` 字段

```json
{
  "id": "dev_tools",
  "name": "开发工具",
  "source": "official"  // 或 "user"
}
```

**方案B**: 通过 ID 前缀区分

- 官方：`official_dev_tools`
- 用户：`user_my_category`

### Q2: 合并更新时的冲突处理？

如果官方更新了某个分类的属性，而用户也修改了，如何处理？

- **选项1**: 用户优先（保留用户修改）
- **选项2**: 官方优先（覆盖用户修改）
- **选项3**: 提示用户选择

### Q3: 是否需要版本控制？

在配置文件中添加版本号，用于检测官方配置更新：

```json
{
  "version": "1.0.0",
  "categories": [...]
}
```

---

## 相关文档

- [架构概览](./overview/README.md)
- [数据流设计](./data-flow/README.md)
- [开发指南](../development/README.md)

---

**文档维护者**: Ghost-Dir Team  
**审核状态**: 待审核
