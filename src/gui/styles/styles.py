"""
统一样式系统
提供主题感知的样式配置和管理
"""
from typing import Dict, Any
from qfluentwidgets import isDarkTheme
from ...common.signals import signal_bus


class StyleManager:
    """样式管理器 - 提供主题感知的样式访问"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化样式管理器"""
        if self._initialized:
            return
        self._initialized = True
        
        # 监听主题变更
        signal_bus.theme_changed.connect(self._on_theme_changed)
    
    def _on_theme_changed(self, theme: str):
        """主题变更回调"""
        # 可以在这里触发样式刷新事件
        pass
    
    # ========== 颜色系统 ==========
    
    @staticmethod
    def get_page_background() -> str:
        """获取页面背景色 - 透明以显示 Mica 材质"""
        return "transparent"
    
    @staticmethod
    def get_background_color() -> str:
        """获取页面背景色（已废弃，使用 get_page_background）"""
        return StyleManager.get_page_background()
    
    @staticmethod
    def get_container_background() -> str:
        """获取容器背景色 - 半透明用于滚动区域"""
        if isDarkTheme():
            return "rgba(0, 0, 0, 0.3)"
        else:
            return "rgba(255, 255, 255, 0.5)"
    
    @staticmethod
    def get_card_background() -> str:
        """获取卡片背景色 - 半透明白色"""
        if isDarkTheme():
            return "rgba(255, 255, 255, 0.05)"
        else:
            return "rgba(255, 255, 255, 0.7)"
    
    @staticmethod
    def get_hover_background() -> str:
        """获取悬停背景色"""
        return "#333333" if isDarkTheme() else "#F0F0F0"
    
    @staticmethod
    def get_border_color() -> str:
        """获取边框颜色"""
        return "#3F3F3F" if isDarkTheme() else "#E0E0E0"
    
    @staticmethod
    def get_text_primary() -> str:
        """获取主要文本颜色"""
        return "#FFFFFF" if isDarkTheme() else "#1F1F1F"
    
    @staticmethod
    def get_text_secondary() -> str:
        """获取次要文本颜色"""
        return "#B0B0B0" if isDarkTheme() else "#606060"
    
    @staticmethod
    def get_text_tertiary() -> str:
        """获取三级文本颜色"""
        return "#808080" if isDarkTheme() else "#909090"
    
    @staticmethod
    def get_text_muted() -> str:
        """获取弱化文本颜色（用于次要信息）"""
        return "#888888" if isDarkTheme() else "#666666"
    
    @staticmethod
    def get_text_disabled() -> str:
        """获取禁用文本颜色"""
        return "#999999"
    
    # ========== 状态颜色 ==========
    
    @staticmethod
    def get_status_colors() -> Dict[str, str]:
        """获取状态颜色映射"""
        return {
            "disconnected": "#E74C3C",  # 红色 - 未连接
            "connected": "#27AE60",     # 绿色 - 已连接
            "ready": "#F39C12",         # 黄色 - 就绪
            "invalid": "#95A5A6",       # 灰色 - 失效
        }
    
    @staticmethod
    def get_status_icons() -> Dict[str, str]:
        """获取状态图标映射"""
        return {
            "disconnected": "🔴",
            "connected": "🟢",
            "ready": "🟡",
            "invalid": "⚪",
        }
    
    @staticmethod
    def get_success_color() -> str:
        """成功色"""
        return "#22C55E"
    
    @staticmethod
    def get_warning_color() -> str:
        """警告色"""
        return "#F59E0B"
    
    @staticmethod
    def get_error_color() -> str:
        """错误色"""
        return "#EF4444"
    
    @staticmethod
    def get_info_color() -> str:
        """信息色"""
        return "#3B82F6"
    
    # ========== 尺寸规范 ==========
    
    @staticmethod
    def get_icon_sizes() -> Dict[str, int]:
        """获取图标尺寸规范"""
        return {
            "sm": 16,
            "md": 24,
            "lg": 32,
            "xl": 48,
        }
    
    @staticmethod
    def get_spacing() -> Dict[str, int]:
        """获取间距规范"""
        return {
            "xs": 4,
            "sm": 8,
            "md": 12,
            "lg": 16,
            "xl": 20,
            "xxl": 24,
            "xxxl": 32,
        }
    
    @staticmethod
    def get_layout_margins() -> Dict[str, int]:
        """获取布局边距规范（Windows 11 Fluent Design）"""
        return {
            "page": 24,          # 页面边距
            "section": 20,       # 区块边距
            "card": 16,          # 卡片内边距
            "compact": 12,       # 紧凑边距
        }
    
    @staticmethod
    def get_list_spacing() -> Dict[str, int]:
        """获取列表间距规范（Windows 11 Fluent Design）"""
        return {
            "group": 20,         # 设置组/列表组之间的间距
            "item": 4,           # 同组内列表项之间的间距
            "section": 16,       # 列表区块之间的间距
        }
    
    @staticmethod
    def get_border_radius() -> Dict[str, int]:
        """获取圆角规范"""
        return {
            "sm": 4,
            "md": 6,
            "lg": 8,
            "xl": 12,
            "xxl": 16,
        }
    
    @staticmethod
    def get_font_family() -> str:
        """获取默认字体族"""
        return '"Segoe UI", "Microsoft YaHei", sans-serif'

    @staticmethod
    def get_font_weights() -> Dict[str, int]:
        """获取字体粗细规范"""
        return {
            "light": 300,
            "regular": 400,
            "normal": 400,
            "medium": 500,
            "semibold": 600,
            "bold": 700,
        }

    @staticmethod
    def get_line_heights() -> Dict[str, float]:
        """获取行高规范（相对于字体大小的倍数）"""
        return {
            "tight": 1.2,
            "normal": 1.4,
            "relaxed": 1.6,
        }

    @staticmethod
    def get_font_sizes() -> Dict[str, int]:
        """获取字体大小规范"""
        return {
            "xs": 10,
            "sm": 12,
            "md": 14,
            "lg": 16,
            "xl": 18,
            "xxl": 20,
            "title": 24,
            "display": 32,
        }

    @staticmethod
    def get_typography_scale() -> Dict[str, Dict[str, int]]:
        """
        获取完整排版规范（字体大小、行高）
        返回包含 size 和 line_height 的字典
        """
        font_sizes = StyleManager.get_font_sizes()
        line_heights = StyleManager.get_line_heights()
        return {
            "caption": {"size": font_sizes["xs"], "line_height": line_heights["tight"]},
            "body-small": {"size": font_sizes["sm"], "line_height": line_heights["normal"]},
            "body": {"size": font_sizes["md"], "line_height": line_heights["normal"]},
            "body-large": {"size": font_sizes["lg"], "line_height": line_heights["normal"]},
            "subtitle": {"size": font_sizes["xl"], "line_height": line_heights["relaxed"]},
            "title": {"size": font_sizes["title"], "line_height": line_heights["relaxed"]},
            "display": {"size": font_sizes["display"], "line_height": line_heights["tight"]},
        }
    
    @staticmethod
    def get_text_hierarchy() -> Dict[str, Dict[str, Any]]:
        """
        获取文字层级规范（Windows 11 Fluent Design）
        定义页面中各类文字的统一样式
        
        Returns:
            包含各层级文字样式的字典，每个层级包含：
            - widget: 推荐使用的 QFluentWidgets 组件
            - size: 字体大小（px）
            - weight: 字体粗细
            - color: 文本颜色类型（primary/secondary/tertiary）
            - usage: 使用场景说明
        """
        font_sizes = StyleManager.get_font_sizes()
        font_weights = StyleManager.get_font_weights()
        
        return {
            # 页面主标题 - 用于页面顶部的主要标题
            "page_title": {
                "widget": "TitleLabel",
                "size": font_sizes["title"],  # 24px
                "weight": font_weights["semibold"],  # 600
                "color": "primary",
                "usage": "页面顶部主标题，如「控制台」「设置」「帮助」"
            },
            
            # 区块标题 - 用于页面内的主要区块标题
            "section_title": {
                "widget": "SubtitleLabel",
                "size": font_sizes["xl"],  # 18px
                "weight": font_weights["semibold"],  # 600
                "color": "primary",
                "usage": "页面内区块标题，如设置组标题"
            },
            
            # 卡片标题 - 用于卡片组件的标题
            "card_title": {
                "widget": "StrongBodyLabel",
                "size": font_sizes["lg"],  # 16px
                "weight": font_weights["semibold"],  # 600
                "color": "primary",
                "usage": "卡片、对话框标题"
            },
            
            # 正文 - 用于主要内容文本
            "body": {
                "widget": "BodyLabel",
                "size": font_sizes["md"],  # 14px
                "weight": font_weights["normal"],  # 400
                "color": "primary",
                "usage": "正文、描述文本"
            },
            
            # 次要文本 - 用于辅助说明
            "body_secondary": {
                "widget": "CaptionLabel",
                "size": font_sizes["md"],  # 14px
                "weight": font_weights["normal"],  # 400
                "color": "secondary",
                "usage": "次要说明文本"
            },
            
            # 小字说明 - 用于提示、标签等
            "caption": {
                "widget": "CaptionLabel",
                "size": font_sizes["sm"],  # 12px
                "weight": font_weights["normal"],  # 400
                "color": "secondary",
                "usage": "小字说明、提示文本、标签"
            },
            
            # 按钮文字
            "button": {
                "widget": "PushButton",
                "size": font_sizes["md"],  # 14px
                "weight": font_weights["normal"],  # 400
                "color": "primary",
                "usage": "按钮文字"
            },
        }
    
    # ========== 组件样式生成器 ==========
    
    @staticmethod
    def get_badge_style(
        bg_color: str = None,
        text_color: str = None,
        size: str = "sm"
    ) -> str:
        """
        生成徽章样式
        
        Args:
            bg_color: 背景颜色（可选）
            text_color: 文本颜色（可选）
            size: 尺寸（sm/md/lg）
        """
        radius = StyleManager.get_border_radius()
        spacing = StyleManager.get_spacing()
        
        bg = bg_color or "rgba(100, 100, 100, 0.2)"
        color = text_color or StyleManager.get_text_secondary()
        
        return f"""
            background-color: {bg};
            color: {color};
            border-radius: {radius['sm']}px;
            padding: {spacing['xs']}px {spacing['sm']}px;
            font-size: 12px;
        """
    
    @staticmethod
    def get_label_style(
        color: str = None,
        size: int = 14,
        weight: str = "normal"
    ) -> str:
        """
        生成标签样式
        
        Args:
            color: 文本颜色（可选）
            size: 字体大小
            weight: 字体粗细
        """
        text_color = color or StyleManager.get_text_primary()
        return f"""
            color: {text_color};
            font-size: {size}px;
            font-weight: {weight};
        """
    
    @staticmethod
    def get_icon_style(size: str = "md") -> str:
        """
        生成图标样式
        
        Args:
            size: 图标尺寸（sm/md/lg/xl）
        """
        sizes = StyleManager.get_icon_sizes()
        icon_size = sizes.get(size, sizes["md"])
        return f"font-size: {icon_size}px;"
    
    @staticmethod
    def get_button_style(variant: str = "primary") -> str:
        """
        获取按钮样式
        
        Args:
            variant: 按钮变体 (primary, secondary, danger, ghost)
        """
        spacing = StyleManager.get_spacing()
        radius = StyleManager.get_border_radius()
        
        base_style = f"""
            QPushButton {{
                padding: {spacing['sm']}px {spacing['lg']}px;
                border-radius: {radius['md']}px;
                font-size: 14px;
            }}
        """
        return base_style
    
    @staticmethod
    def get_card_style() -> str:
        """获取卡片样式"""
        bg = StyleManager.get_card_background()
        border = StyleManager.get_border_color()
        radius = StyleManager.get_border_radius()
        
        return f"""
            QWidget {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: {radius['lg']}px;
            }}
        """
    
    @staticmethod
    def get_badge_style(status: str) -> str:
        """
        获取徽章样式
        
        Args:
            status: 状态类型 (disconnected, connected, ready, invalid)
        """
        colors = StyleManager.get_status_colors()
        radius = StyleManager.get_border_radius()
        spacing = StyleManager.get_spacing()
        
        color = colors.get(status, colors["invalid"])
        
        return f"""
            QWidget {{
                background-color: {color}20;
                border-radius: {radius['sm']}px;
                padding: {spacing['xs']}px {spacing['sm']}px;
            }}
            QLabel {{
                color: {color};
                background: transparent;
                border: none;
            }}
        """


# ========== 预定义样式常量 ==========

# 窗口尺寸
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# 表格样式
TABLE_ROW_HEIGHT = 60
TABLE_HEADER_HEIGHT = 40

# 动画时长
ANIMATION_DURATION = 200  # 毫秒

# 阴影
SHADOW_BLUR = 10
SHADOW_OFFSET = 2


# ========== 工具函数 ==========

def apply_page_style(widget) -> None:
    """
    应用页面样式到 widget
    
    Args:
        widget: 要应用样式的 widget
    """
    bg_color = StyleManager.get_page_background()
    widget.setStyleSheet(f"background-color: {bg_color};")


def apply_container_style(widget) -> None:
    """
    应用容器样式（半透明背景）
    
    Args:
        widget: 要应用样式的 widget
    """
    bg_color = StyleManager.get_container_background()
    widget.setStyleSheet(f"background-color: {bg_color};")


def apply_page_layout(layout, spacing: str = "group"):
    """
    统一应用页面布局规范
    
    Args:
        layout: 布局对象 (QVBoxLayout, ExpandLayout 等)
        spacing: 间距类型 (group/section/item)
    """
    margins = StyleManager.get_layout_margins()
    spacing_val = StyleManager.get_list_spacing().get(spacing, 20)
    
    layout.setContentsMargins(margins["page"], margins["page"], margins["page"], margins["page"])
    layout.setSpacing(spacing_val)


def apply_muted_text_style(widget, size: int = 12) -> None:
    """
    应用弱化文本样式
    
    Args:
        widget: 要应用样式的 widget
        size: 字体大小
    """
    color = StyleManager.get_text_muted()
    widget.setStyleSheet(f"color: {color}; font-size: {size}px;")


def get_spacing(size: str = "md") -> int:
    """
    获取间距值的快捷函数
    
    Args:
        size: 间距大小 (xs, sm, md, lg, xl, xxl, xxxl)
    
    Returns:
        间距像素值
    """
    return StyleManager.get_spacing().get(size, 12)


def get_radius(size: str = "md") -> int:
    """
    获取圆角值的快捷函数

    Args:
        size: 圆角大小 (sm, md, lg, xl, xxl)

    Returns:
        圆角像素值
    """
    return StyleManager.get_border_radius().get(size, 6)


# ========== 字体工具函数 ==========

def get_font_size(size: str = "md") -> int:
    """
    获取字体大小的快捷函数

    Args:
        size: 字体大小 (xs, sm, md, lg, xl, xxl, title, display)

    Returns:
        字体大小像素值
    """
    return StyleManager.get_font_sizes().get(size, 14)


def get_font_weight(weight: str = "normal") -> int:
    """
    获取字体粗细的快捷函数

    Args:
        weight: 字体粗细 (light, regular/normal, medium, semibold, bold)

    Returns:
        字体粗细数值
    """
    return StyleManager.get_font_weights().get(weight, 400)


def apply_font_style(
    widget,
    size: str = "md",
    weight: str = "normal",
    color: str = None
) -> None:
    """
    应用字体样式到 widget

    Args:
        widget: 要应用样式的 widget
        size: 字体大小 (xs, sm, md, lg, xl, xxl, title, display)
        weight: 字体粗细 (light, regular/normal, medium, semibold, bold)
        color: 文本颜色（可选）
    """
    font_family = StyleManager.get_font_family()
    font_size = get_font_size(size)
    font_weight = get_font_weight(weight)
    text_color = color or StyleManager.get_text_primary()

    widget.setStyleSheet(
        f"font-family: {font_family}; "
        f"font-size: {font_size}px; "
        f"font-weight: {font_weight}; "
        f"color: {text_color};"
    )


def apply_typography_style(widget, typography: str = "body", color: str = None) -> None:
    """
    应用排版规范样式到 widget

    Args:
        widget: 要应用样式的 widget
        typography: 排版类型 (caption, body-small, body, body-large, subtitle, title, display)
        color: 文本颜色（可选）
    """
    scale = StyleManager.get_typography_scale()
    typo_data = scale.get(typography, scale["body"])

    font_family = StyleManager.get_font_family()
    text_color = color or StyleManager.get_text_primary()

    widget.setStyleSheet(
        f"font-family: {font_family}; "
        f"font-size: {typo_data['size']}px; "
        f"line-height: {typo_data['line_height']}; "
        f"color: {text_color};"
    )


def get_font_style(
    size: str = "md",
    weight: str = "normal",
    color: str = None
) -> str:
    """
    获取字体样式字符串（用于内联样式）

    Args:
        size: 字体大小 (xs, sm, md, lg, xl, xxl, title, display)
        weight: 字体粗细 (light, regular/normal, medium, semibold, bold)
        color: 文本颜色（可选）

    Returns:
        CSS 样式字符串
    """
    font_family = StyleManager.get_font_family()
    font_size = get_font_size(size)
    font_weight = get_font_weight(weight)
    text_color = color or StyleManager.get_text_primary()

    return (
        f"font-family: {font_family}; "
        f"font-size: {font_size}px; "
        f"font-weight: {font_weight}; "
        f"color: {text_color};"
    )
