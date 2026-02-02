"""
统一样式系统
按功能模块化组织，支持主题感知、多尺寸间距、标准组件样式和图标系统。
"""

from src.gui.styles.manager import StyleManager
from src.gui.styles.stylesheet import window_style_sheet, link_table_style_sheet
from src.gui.styles.utils.color_utils import *
from src.gui.styles.utils.spacing_utils import *
from src.gui.styles.utils.typography_utils import *
from src.gui.styles.utils.icon_utils import *
from src.gui.styles.appliers.layout import *
from src.gui.styles.appliers.component import *
from src.gui.styles.appliers.icon import *
from src.gui.styles.appliers.common import (
    apply_transparent_style,
    apply_transparent_background_only,
    apply_no_border
)

# ========== 预定义常量 (从旧 styles.py 迁移) ==========
# 窗口尺寸
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# 表格样式
TABLE_ROW_HEIGHT = 60
TABLE_HEADER_HEIGHT = 40

# 动画时长
ANIMATION_DURATION = 200

# 阴影
SHADOW_BLUR = 10
SHADOW_OFFSET = 2

__all__ = [
    'StyleManager',
    # 颜色相关
    'get_page_background', 'get_container_background', 'get_card_background',
    'get_hover_background', 'get_border_color', 'get_text_primary',
    'get_text_secondary', 'get_text_tertiary', 'get_text_muted',
    'get_text_disabled', 'get_status_colors', 'get_success_color',
    'get_warning_color', 'get_error_color', 'get_info_color',
    'get_surface_color', 'get_outline_color', 'get_divider_color',
    'get_shadow_color', 'get_accent_color', 'get_icon_background', 'get_item_selected_background',
    # 间距与布局相关
    'get_spacing', 'get_padding', 'get_margin', 'get_radius',
    'get_layout_margins', 'get_list_spacing', 'get_card_padding', 'get_badge_padding',
    'apply_page_style', 'apply_container_style', 'apply_page_layout',
    'apply_spacing', 'apply_padding', 'apply_layout_margins',
    # 排版相关
    'get_font_family', 'get_font_size', 'get_font_weight', 'get_line_height',
    'get_typography_scale', 'get_text_hierarchy', 'get_font_style',
    'apply_font_style', 'apply_muted_text_style',
    # 图标相关
    'get_icon_size', 'get_icon_color', 'get_icon_spacing', 'get_icon_state',
    'get_status_icon', 'apply_icon_style', 'get_icon_state_style',
    'create_icon_with_text',
    # 组件相关
    'apply_card_style', 'apply_badge_style', 'apply_accent_badge_style', 'get_content_width',
]
