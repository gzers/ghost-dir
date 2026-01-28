# 文字组件快速参考

## 快速选择指南

| 使用场景 | 组件 | 大小 | 粗细 | 示例 |
|---------|------|------|------|------|
| 页面主标题 | `TitleLabel` | 24px | 600 | 「控制台」「设置」 |
| 区块标题 | `SubtitleLabel` | 18px | 600 | 「目录配置」「外观设置」 |
| 卡片标题 | `StrongBodyLabel` | 16px | 600 | 「智能扫描」「关于」 |
| 正文 | `BodyLabel` | 14px | 400 | 描述文本、说明 |
| 次要文本 | `CaptionLabel` | 14px | 400 | 辅助说明（灰色） |
| 小字说明 | `CaptionLabel` | 12px | 400 | 版本号、时间戳 |

## 代码模板

### 页面主标题
```python
from qfluentwidgets import TitleLabel
from ...i18n import t

title = TitleLabel(t("page.title"))
```

### 区块标题
```python
from qfluentwidgets import SubtitleLabel

section_title = SubtitleLabel("区块标题")
```

### 卡片标题
```python
from qfluentwidgets import StrongBodyLabel

card_title = StrongBodyLabel("卡片标题")
```

### 正文
```python
from qfluentwidgets import BodyLabel

description = BodyLabel("这是一段描述文本")
```

### 次要文本（灰色）
```python
from qfluentwidgets import CaptionLabel
from ...styles import StyleManager

secondary = CaptionLabel("次要说明")
secondary.setStyleSheet(f"color: {StyleManager.get_text_secondary()};")
```

### 小字说明
```python
from qfluentwidgets import CaptionLabel

caption = CaptionLabel("v2.4.1")
```

## 记住这个规则

**页面标题 = TitleLabel**  
**卡片标题 = StrongBodyLabel**  
**区块标题 = SubtitleLabel**  
**正文 = BodyLabel**

详细文档：`docs/TEXT_HIERARCHY.md`
