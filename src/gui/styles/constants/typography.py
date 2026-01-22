"""
排版系统
包含字体、字号、字重、行高、文字层级规范
"""

FONT_FAMILY = '"Segoe UI", "Microsoft YaHei", sans-serif'

FONT_SIZES = {
    "xs": 10,
    "sm": 12,
    "md": 14,
    "lg": 16,
    "xl": 18,
    "xxl": 20,
    "title": 24,
    "display": 32,
}

FONT_WEIGHTS = {
    "light": 300,
    "regular": 400,
    "normal": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
}

LINE_HEIGHTS = {
    "tight": 1.2,
    "normal": 1.4,
    "relaxed": 1.6,
}

# ========== 文字阶梯 (Typography Scale) ==========
TYPOGRAPHY_SCALE = {
    "caption": {"size": FONT_SIZES["xs"], "line_height": LINE_HEIGHTS["tight"]},
    "body-small": {"size": FONT_SIZES["sm"], "line_height": LINE_HEIGHTS["normal"]},
    "body": {"size": FONT_SIZES["md"], "line_height": LINE_HEIGHTS["normal"]},
    "body-large": {"size": FONT_SIZES["lg"], "line_height": LINE_HEIGHTS["normal"]},
    "subtitle": {"size": FONT_SIZES["xl"], "line_height": LINE_HEIGHTS["relaxed"]},
    "title": {"size": FONT_SIZES["title"], "line_height": LINE_HEIGHTS["relaxed"]},
    "display": {"size": FONT_SIZES["display"], "line_height": LINE_HEIGHTS["tight"]},
}

# ========== 文字层级 (Text Hierarchy) ==========
TEXT_HIERARCHY = {
    "page_title": {
        "widget": "TitleLabel",
        "size": FONT_SIZES["title"],
        "weight": FONT_WEIGHTS["semibold"],
        "color": "primary",
    },
    "section_title": {
        "widget": "SubtitleLabel",
        "size": FONT_SIZES["xl"],
        "weight": FONT_WEIGHTS["semibold"],
        "color": "primary",
    },
    "card_title": {
        "widget": "StrongBodyLabel",
        "size": FONT_SIZES["lg"],
        "weight": FONT_WEIGHTS["semibold"],
        "color": "primary",
    },
    "body": {
        "widget": "BodyLabel",
        "size": FONT_SIZES["md"],
        "weight": FONT_WEIGHTS["normal"],
        "color": "primary",
    },
    "body_secondary": {
        "widget": "CaptionLabel",
        "size": FONT_SIZES["md"],
        "weight": FONT_WEIGHTS["normal"],
        "color": "secondary",
    },
    "caption": {
        "widget": "CaptionLabel",
        "size": FONT_SIZES["sm"],
        "weight": FONT_WEIGHTS["normal"],
        "color": "secondary",
    },
    "button": {
        "widget": "PushButton",
        "size": FONT_SIZES["md"],
        "weight": FONT_WEIGHTS["normal"],
        "color": "primary",
    },
}
