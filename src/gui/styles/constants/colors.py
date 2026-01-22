"""
颜色系统
包含基础颜色、文本颜色、状态颜色、语义化颜色
"""
from qfluentwidgets import isDarkTheme

# ========== 基础颜色 ==========
# 页面主背景色 - 稳定的深色底层
def get_page_background():
    return "#121212" if isDarkTheme() else "#FFFFFF"

def get_container_background():
    """获取容器背景色 - 默认透明，仅作为布局容器"""
    return "transparent"

def get_card_background():
    """获取卡片背景色 - 亚克力/玻璃态半透明"""
    if isDarkTheme():
        return "rgba(35, 35, 35, 0.8)"  # 稍微加深且增加不透明度
    else:
        return "rgba(255, 255, 255, 0.85)"

def get_hover_background():
    return "rgba(255, 255, 255, 0.1)" if isDarkTheme() else "rgba(0, 0, 0, 0.05)"

def get_border_color():
    """获取边框颜色 - 显著增强对比度以确保可见"""
    if isDarkTheme():
        return "rgba(255, 255, 255, 0.25)" # 提升到 25% 不透明度
    else:
        return "rgba(0, 0, 0, 0.2)"

# ========== 文本颜色 ==========
def get_text_primary():
    return "#FFFFFF" if isDarkTheme() else "#1F1F1F"

def get_text_secondary():
    return "#B0B0B0" if isDarkTheme() else "#606060"

def get_text_tertiary():
    return "#808080" if isDarkTheme() else "#909090"

def get_text_muted():
    return "#888888" if isDarkTheme() else "#666666"

TEXT_DISABLED = "#999999"

# ========== 状态颜色 ==========
STATUS_COLORS = {
    "disconnected": "#E74C3C",  # 红色 - 未连接
    "connected": "#27AE60",     # 绿色 - 已连接
    "ready": "#F39C12",         # 黄色 - 就绪
    "invalid": "#95A5A6",       # 灰色 - 失效
}

SUCCESS_COLOR = "#22C55E"
WARNING_COLOR = "#F59E0B"
ERROR_COLOR = "#EF4444"
INFO_COLOR = "#3B82F6"

# ========== 语义化颜色 (Semantic Colors) ==========
def get_surface_color():
    """页面表面主色"""
    return "rgba(45, 45, 45, 0.7)" if isDarkTheme() else "rgba(255, 255, 255, 0.7)"

def get_surface_variant_color():
    """变体表面色"""
    return "rgba(50, 50, 50, 0.8)" if isDarkTheme() else "rgba(243, 243, 243, 0.8)"

def get_outline_color():
    """轮廓线颜色"""
    return "rgba(255, 255, 255, 0.08)" if isDarkTheme() else "rgba(0, 0, 0, 0.08)"

def get_divider_color():
    """分隔线颜色"""
    return "rgba(255, 255, 255, 0.06)" if isDarkTheme() else "rgba(0, 0, 0, 0.06)"

def get_shadow_color():
    """阴影颜色"""
    return "rgba(0, 0, 0, 0.3)" if isDarkTheme() else "rgba(0, 0, 0, 0.1)"

ACCENT_COLOR = "#0078D4"  # 品牌强调色
