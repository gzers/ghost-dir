"""
自定义通知管理器 (Notification Manager)
实现全应用统一的置顶居中 (Top Center) 通知布局
"""
from PySide6.QtCore import QPoint, Qt
from qfluentwidgets import InfoBar, InfoBarManager, InfoBarPosition


@InfoBarManager.register('TopCenter')
class TopCenterInfoBarManager(InfoBarManager):
    """ 自定义置顶居中通知管理器 """

    def _pos(self, infoBar: InfoBar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        # 计算水平居中位置
        x = (parentSize.width() - infoBar.width()) // 2
        # 固定顶部边距
        y = 24

        # 获取当前窗口中所有通知的索引，累加高度以实现堆叠
        if p in self.infoBars:
            index = self.infoBars[p].index(infoBar)
            for bar in self.infoBars[p][0:index]:
                y += (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        """ 设置动画起始位置（从上方滑入） """
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() - 32)
