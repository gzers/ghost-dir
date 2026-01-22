"""
间距系统
包含基础间距、内边距 (Padding)、外边距 (Margin)
"""

# ========== 基础间距阶梯 (Spacing Scale) ==========
SPACING_SCALE = {
    "none": 0,      # 0px
    "xxs": 2,       # 2px
    "xs": 4,        # 4px
    "sm": 8,        # 8px
    "md": 12,       # 12px
    "lg": 16,       # 16px
    "xl": 20,       # 20px
    "xxl": 24,      # 24px
    "xxxl": 32,     # 32px
}

# ========== 内边距规范 (Padding Scale) ==========
# 格式: (top, right, bottom, left)
PADDING_SCALE = {
    "none": (0, 0, 0, 0),
    "xs": (4, 8, 4, 8),
    "sm": (8, 12, 8, 12),
    "md": (12, 16, 12, 16),
    "lg": (16, 20, 16, 20),
    "xl": (20, 24, 20, 24),
}

# ========== 外边距规范 (Margin Scale) ==========
MARGIN_SCALE = {
    "none": (0, 0, 0, 0),
    "xs": (4, 4, 4, 4),
    "sm": (8, 8, 8, 8),
    "md": (12, 12, 12, 12),
    "lg": (16, 16, 16, 16),
    "xl": (20, 20, 20, 20),
}

# ========== 布局特定规范 (Layout Margins) ==========
LAYOUT_MARGINS = {
    "page": 24,          # 页面边距
    "section": 20,       # 区块边距
    "card": 16,          # 卡片默认内边距
    "compact": 12,       # 紧凑边距
}

LIST_SPACING = {
    "group": 20,         # 组间距
    "item": 4,           # 项间距
    "section": 16,       # 区块间距
}

# ========== 圆角规范 ==========
BORDER_RADIUS = {
    "none": 0,
    "xs": 2,
    "sm": 4,
    "md": 6,
    "lg": 8,
    "xl": 12,
    "xxl": 16,
    "xxxl": 24,
    "round": 9999,
}
