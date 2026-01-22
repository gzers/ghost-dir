"""
组件规范
定义各 UI 组件的标准样式规范 (Padding, Margin, Height, etc.)
"""
from .spacing import PADDING_SCALE, BORDER_RADIUS

COMPONENT_STYLES = {
    "card": {
        "padding": PADDING_SCALE["xl"],  # (20, 24, 20, 24)
        "margin": (0, 0, 12, 0),         # 下边距 12px
        "border_radius": BORDER_RADIUS["lg"],
        "border_width": 1
    },
    "button": {
        "padding_sm": (6, 12, 6, 12),
        "padding_md": (8, 16, 8, 16),
        "padding_lg": (10, 20, 10, 20),
        "height_sm": 28,
        "height_md": 32,
        "height_lg": 40,
        "border_radius": BORDER_RADIUS["sm"]
    },
    "input": {
        "padding": (8, 12, 8, 12),
        "height": 32,
        "border_radius": BORDER_RADIUS["sm"]
    },
    "list_item": {
        "padding": (12, 16, 12, 16),
        "height": 48,
        "spacing": 8
    },
    "window": {
        "min_width": 1000,
        "min_height": 700
    },
    "table": {
        "row_height": 60,
        "header_height": 40
    },
    # 页面/内容宽度等级 (用于说明性页面或工具类页面的容器约束)
    "content_width": {
        "narrow": 560,     # 关于页、设置详情等紧凑内容
        "medium": 840,     # 向导、中等复杂列表等
        "full": None       # 全宽模式 (默认)
    },
    "badge": {
        "padding": (2, 6, 2, 6),         # (top, right, bottom, left)
        "border_radius": BORDER_RADIUS["xs"],
        "spacing": 4
    }
}

# ========== 动画规范 ==========
ANIMATION_DURATION = 200  # 毫秒

# ========== 阴影规范 ==========
SHADOW_BLUR = 10
SHADOW_OFFSET = 2
