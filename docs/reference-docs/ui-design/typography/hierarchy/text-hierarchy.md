

# 文本层级规范

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`


本文档定义了项目中统一的文字样式规范，遵循 Windows 11 Fluent Design 设计原则。

## 规范概览

所有文字层级规范定义在 `src/gui/styles/styles.py` 的 `StyleManager.get_text_hierarchy()` 方法中。

## 文字层级

### 1. 页面主标题 (page_title)
- **组件**: `TitleLabel`
- **字体大小**: 24px
- **字体粗细**: 600 (Semibold)
- **颜色**: Primary
- **使用场景**: 页面顶部的主要标题
- **示例**: 「控制台」「设置」「帮助」「模版库」「智能向导」

```python
from qfluentwidgets import TitleLabel
title = TitleLabel(t("console.title"))
```

### 2. 区块标题 (section_title)
- **组件**: `SubtitleLabel`
- **字体大小**: 18px
- **字体粗细**: 600 (Semibold)
- **颜色**: Primary
- **使用场景**: 页面内的主要区块标题
- **示例**: 设置页面中的「目录配置」「外观设置」等组标题

```python
from qfluentwidgets import SubtitleLabel
section_title = SubtitleLabel("外观设置")
```

### 3. 卡片标题 (card_title)
- **组件**: `StrongBodyLabel`
- **字体大小**: 16px
- **字体粗细**: 600 (Semibold)
- **颜色**: Primary
- **使用场景**: 卡片组件、对话框的标题
- **示例**: 扫描进度卡片的「智能扫描」标题

```python
from qfluentwidgets import StrongBodyLabel
card_title = StrongBodyLabel("智能扫描")
```

### 4. 正文 (body)
- **组件**: `BodyLabel`
- **字体大小**: 14px
- **字体粗细**: 400 (Normal)
- **颜色**: Primary
- **使用场景**: 正文、描述文本
- **示例**: 卡片内的说明文字、列表项的主要内容

```python
from qfluentwidgets import BodyLabel
description = BodyLabel("这是一段描述文本")
```

### 5. 次要文本 (body_secondary)
- **组件**: `CaptionLabel`
- **字体大小**: 14px
- **字体粗细**: 400 (Normal)
- **颜色**: Secondary
- **使用场景**: 次要说明文本
- **示例**: 辅助性的说明信息

```python
from qfluentwidgets import CaptionLabel
from ...styles import StyleManager
secondary_text = CaptionLabel("辅助说明")
secondary_text.setStyleSheet(f"color: {StyleManager.get_text_secondary()};")
```

### 6. 小字说明 (caption)
- **组件**: `CaptionLabel`
- **字体大小**: 12px
- **字体粗细**: 400 (Normal)
- **颜色**: Secondary
- **使用场景**: 小字说明、提示文本、标签
- **示例**: 时间戳、状态标签、版本号

```python
from qfluentwidgets import CaptionLabel
caption = CaptionLabel("v2.4.1")
```

### 7. 按钮文字 (button)
- **组件**: `PushButton`
- **字体大小**: 14px
- **字体粗细**: 400 (Normal)
- **颜色**: Primary
- **使用场景**: 按钮文字
- **示例**: 所有按钮组件

```python
from qfluentwidgets import PushButton
button = PushButton("确定")
```

## 使用原则

### 1. 统一性
- **页面标题必须使用 `TitleLabel`**，不要使用 `SubtitleLabel`
- 同一层级的文字在整个应用中保持一致

### 2. 层级清晰
- 页面标题 > 区块标题 > 卡片标题 > 正文
- 避免跳级使用（如页面标题直接跳到小字说明）

### 3. 颜色使用
- **Primary**: 主要内容，最重要的信息
- **Secondary**: 次要内容，辅助说明
- **Tertiary**: 三级内容，弱化信息

通过 `StyleManager` 获取颜色：
```python
from ...styles import StyleManager

primary_color = StyleManager.get_text_primary()
secondary_color = StyleManager.get_text_secondary()
tertiary_color = StyleManager.get_text_tertiary()
```

### 4. 自定义样式
如需自定义文字样式，使用 `apply_font_style` 工具函数：

```python
from ...styles import apply_font_style, StyleManager

label = QLabel("自定义文字")
apply_font_style(
    label,
    size="lg",  # xs, sm, md, lg, xl, xxl, title, display
    weight="semibold",  # light, regular, normal, medium, semibold, bold
    color=StyleManager.get_text_primary()
)
```

## 迁移指南

### 从旧代码迁移

1. **页面标题**
   ```python
   # 旧代码（不统一）
   title = SubtitleLabel("页面标题")
   
   # 新代码（统一）
   from qfluentwidgets import TitleLabel
   title = TitleLabel(t("page.title"))
   ```

2. **卡片标题**
   ```python
   # 旧代码
   title = SubtitleLabel("卡片标题")
   
   # 新代码
   from qfluentwidgets import StrongBodyLabel
   title = StrongBodyLabel("卡片标题")
   ```

## 检查清单

在创建或修改 UI 时，请确保：

- [ ] 页面主标题使用 `TitleLabel`
- [ ] 区块标题使用 `SubtitleLabel`
- [ ] 卡片标题使用 `StrongBodyLabel`
- [ ] 正文使用 `BodyLabel`
- [ ] 小字说明使用 `CaptionLabel`
- [ ] 文字颜色使用 `StyleManager` 提供的颜色
- [ ] 自定义样式使用 `apply_font_style` 工具函数

## 相关文件

- `src/gui/styles/styles.py` - 样式管理器和文字层级定义
- `src/gui/views/` - 各个视图的实现
- `src/gui/i18n/` - 国际化文本资源

