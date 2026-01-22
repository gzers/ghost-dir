# 文字风格统一处理总结

## 问题分析

在项目中发现以下文字风格不统一的问题：

1. **页面标题不统一**：
   - `console_view.py` 使用 `TitleLabel`
   - `settings_view.py` 使用 `TitleLabel`
   - `help_view.py` 使用 `TitleLabel`
   - `library_view.py` 使用 `SubtitleLabel` ❌
   - `wizard_view.py` 使用 `SubtitleLabel` ❌

2. **卡片标题不统一**：
   - `scan_progress.py` 使用 `SubtitleLabel` ❌（应该使用更小的标题）

3. **缺少明确的文字层级规范**

## 解决方案

### 1. 定义文字层级规范

在 `src/gui/styles/styles.py` 中添加了 `get_text_hierarchy()` 方法，定义了完整的文字层级：

- **page_title**: 页面主标题 - `TitleLabel` (24px, Semibold)
- **section_title**: 区块标题 - `SubtitleLabel` (18px, Semibold)
- **card_title**: 卡片标题 - `StrongBodyLabel` (16px, Semibold)
- **body**: 正文 - `BodyLabel` (14px, Normal)
- **body_secondary**: 次要文本 - `CaptionLabel` (14px, Normal, Secondary Color)
- **caption**: 小字说明 - `CaptionLabel` (12px, Normal, Secondary Color)
- **button**: 按钮文字 - `PushButton` (14px, Normal)

### 2. 统一页面标题

修改了以下文件，将页面标题统一为 `TitleLabel`：

#### library_view.py
```python
# 修改前
from qfluentwidgets import SubtitleLabel
self.title_label = SubtitleLabel(t("library.title"))

# 修改后
from qfluentwidgets import TitleLabel
self.title_label = TitleLabel(t("library.title"))
```

#### wizard_view.py
```python
# 修改前
from qfluentwidgets import SubtitleLabel
self.title_label = SubtitleLabel(t("wizard.title"))

# 修改后
from qfluentwidgets import TitleLabel
self.title_label = TitleLabel(t("wizard.title"))
```

### 3. 统一卡片标题

修改了 `scan_progress.py`，将卡片标题改为 `StrongBodyLabel`：

```python
# 修改前
from qfluentwidgets import SubtitleLabel
self.title_label = SubtitleLabel("智能扫描")

# 修改后
from qfluentwidgets import StrongBodyLabel
self.title_label = StrongBodyLabel("智能扫描")
```

### 4. 创建规范文档

创建了 `docs/TEXT_HIERARCHY.md` 文档，详细说明：
- 各层级文字的使用场景
- 推荐的组件和样式参数
- 使用示例和代码片段
- 迁移指南和检查清单

## 修改文件清单

1. ✅ `src/gui/styles/styles.py` - 添加 `get_text_hierarchy()` 方法
2. ✅ `src/gui/views/library/library_view.py` - 页面标题改为 `TitleLabel`
3. ✅ `src/gui/views/wizard/wizard_view.py` - 页面标题改为 `TitleLabel`
4. ✅ `src/gui/views/wizard/widgets/scan_progress.py` - 卡片标题改为 `StrongBodyLabel`
5. ✅ `src/gui/views/help/widgets/about_card.py` - 卡片内应用名称改为 `StrongBodyLabel`
6. ✅ `src/gui/views/setting_view.py` - 卡片内应用名称改为 `StrongBodyLabel`
7. ✅ `docs/TEXT_HIERARCHY.md` - 新建文字层级规范文档
8. ✅ `docs/TEXT_QUICK_REFERENCE.md` - 新建快速参考文档

## 效果

### 统一前
- 页面标题大小不一致（有的 24px，有的 18px）
- 缺少明确的使用规范
- 开发者不清楚应该使用哪个组件

### 统一后
- ✅ 所有页面标题统一使用 `TitleLabel` (24px)
- ✅ 卡片标题统一使用 `StrongBodyLabel` (16px)
- ✅ 有明确的文字层级规范文档
- ✅ 开发者可以快速查阅使用规范

## 使用建议

在后续开发中：

1. **创建新页面时**，参考 `docs/TEXT_HIERARCHY.md` 选择合适的文字组件
2. **页面主标题必须使用 `TitleLabel`**
3. **卡片标题使用 `StrongBodyLabel`**
4. **区块标题使用 `SubtitleLabel`**
5. **正文使用 `BodyLabel`**

## 验证方法

可以通过以下命令搜索项目中的标题使用情况：

```bash
# 搜索页面标题
grep -r "TitleLabel" src/gui/views/

# 搜索区块标题
grep -r "SubtitleLabel" src/gui/views/

# 搜索卡片标题
grep -r "StrongBodyLabel" src/gui/views/
```

确保：
- 所有主视图文件（`*_view.py`）的页面标题都使用 `TitleLabel`
- 卡片组件的标题使用 `StrongBodyLabel`
- 设置组等区块标题使用 `SubtitleLabel`
