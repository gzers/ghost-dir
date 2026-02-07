"""
图标系统
包含图标尺寸、颜色、间距、状态规范
"""
from qfluentwidgets import FluentIcon

# ========== 图标尺寸 (Icon Sizes) ==========
ICON_SIZES = {
    "xs": 12,      # 极小图标（徽章、内联图标）
    "sm": 16,      # 小图标（列表项、次要按钮）
    "md": 20,      # 中等图标（默认）
    "lg": 24,      # 大图标（主要按钮、工具栏）
    "xl": 32,      # 特大图标（卡片头部、功能区）
    "xxl": 48,     # 极大图标（空状态、引导）
    "xxxl": 64,    # 巨大图标（应用图标、品牌展示）
}

# ========== 图标颜色 (Icon Colors) ==========
# 语义化引用，具体的颜色值在 color_utils 中根据主题动态计算
ICON_COLOR_LEVELS = ["primary", "secondary", "tertiary", "disabled"]
ICON_STATUS_LEVELS = ["accent", "success", "warning", "error", "info"]

# ========== 图标间距 (Icon Spacing) ==========
ICON_SPACING = {
    "icon_text": 8,      # 图标与文本的间距
    "icon_icon": 12,     # 多个图标并排时的间距
    "icon_edge": 16,     # 图标与容器边缘的间距
}

# ========== 图标状态 (Icon States) ==========
ICON_STATES = {
    "default": {
        "opacity": 1.0,
        "scale": 1.0
    },
    "hover": {
        "opacity": 0.8,
        "scale": 1.05
    },
    "active": {
        "opacity": 0.6,
        "scale": 0.95
    },
    "disabled": {
        "opacity": 0.38,
        "scale": 1.0
    }
}

# ========== 状态图标映射 (从旧代码迁移) ==========
STATUS_ICONS = {
    "disconnected": "🔴",
    "connected": "🟢",
    "ready": "🟡",
    "invalid": FluentIcon.INFO,
    "error": FluentIcon.CLOSE,
}
