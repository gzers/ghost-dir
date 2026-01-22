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
