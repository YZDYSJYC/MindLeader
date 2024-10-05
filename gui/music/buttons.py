# coding=utf-8
# 作者: 拓跋龙
# 功能: 自定义音乐组件

from qfluentwidgets import theme
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QToolButton

from source.frame.image_manager import register_image

color_map = {
    'dark': (255, 255, 255),
    'light': (0, 0, 0),
}

class PlayButton(QToolButton):
    """ Play button """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isPlaying = False
        self.isEnter = False
        self.isPressed = False
        _theme = theme().value.lower()
        self.iconPixmaps = [
            QPixmap(f'./config/image/play_{_theme}.png'),
            QPixmap(f'./config/image/pause_{_theme}.png')
        ]
        self.setToolTip('播放')
        self.setFixedSize(65, 65)
        self.setStyleSheet(
            "QToolButton{border:none;margin:0;background:transparent}")
        self.installEventFilter(self)

        register_image(self, self.change_theme)

    def setPlay(self, play: bool = True):
        """ set play state """
        self.isPlaying = play
        self.setToolTip('暂停' if play else '播放')
        self.update()

    def eventFilter(self, obj, e):
        if obj == self and self.isEnabled():
            if e.type() == QEvent.MouseButtonRelease and e.button() == Qt.LeftButton:
                self.isPlaying = not self.isPlaying
                self.isPressed = False
                self.update()
                return False
            if e.type() == QEvent.MouseButtonPress and e.button() == Qt.LeftButton:
                # self.hideToolTip()
                self.isPressed = True
                self.update()
                return False

        return super().eventFilter(obj, e)

    def enterEvent(self, e):
        super().enterEvent(e)
        self.isEnter = True
        self.update()

    def leaveEvent(self, e):
        super().leaveEvent(e)
        self.isEnter = False
        self.update()

    def paintEvent(self, e):
        """ paint button """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        _theme = theme().value.lower()
        r, g, b = color_map[_theme]
        if self.isPressed:
            painter.setPen(QPen(QColor(r, g, b, 120), 2))
            painter.drawEllipse(1, 1, 62, 62)
        elif self.isEnter:
            # paint a two color circle
            painter.setPen(QPen(QColor(r, g, b, 18)))
            painter.drawEllipse(1, 1, 62, 62)
            # paint background
            painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
            painter.drawEllipse(2, 2, 61, 61)
            painter.setPen(QPen(QColor(0, 0, 0, 39)))
            painter.drawEllipse(1, 1, 63, 63)
        else:
            painter.setPen(QPen(QColor(r, g, b, 255), 2))
            painter.drawEllipse(1, 1, 62, 62)

        # paint icon
        if not self.isPressed:
            iconPix = self.iconPixmaps[self.isPlaying]
            painter.drawPixmap(1, 1, 63, 63, iconPix)
        else:
            iconPix = self.iconPixmaps[self.isPlaying].scaled(
                58, 58, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(3, 3, 59, 59, iconPix)

    def change_theme(self, theme):
        self.iconPixmaps = [
            QPixmap(f'./config/image/play_{theme}.png'),
            QPixmap(f'./config/image/pause_{theme}.png')
        ]
        self.update()

class BasicButton(QToolButton):
    """ Basic circle button """

    def __init__(self, iconPath: str, parent=None):
        super().__init__(parent)
        self.isEnter = False
        self.isPressed = False
        self.iconPixmap = QPixmap(iconPath)
        self.setFixedSize(47, 47)

    def enterEvent(self, e):
        super().enterEvent(e)
        self.isEnter = True
        self.update()

    def leaveEvent(self, e):
        super().leaveEvent(e)
        self.isEnter = False
        self.update()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.isPressed = True
        self.update()

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        """ paint button """
        image = self.iconPixmap
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        painter.setPen(Qt.NoPen)
        if self.isPressed:
            bgBrush = QBrush(QColor(0, 0, 0, 45))
            painter.setBrush(bgBrush)
            painter.drawEllipse(2, 2, 42, 42)
            image = self.iconPixmap.scaled(
                43, 43, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        elif self.isEnter:
            painter.setPen(QPen(QColor(0, 0, 0, 38)))
            bgBrush = QBrush(QColor(0, 0, 0, 26))
            painter.setBrush(bgBrush)
            painter.drawEllipse(1, 1, 44, 44)
        painter.setPen(Qt.NoPen)

        # paint icon
        if not self.isPressed:
            painter.drawPixmap(1, 1, 45, 45, image)
        else:
            painter.drawPixmap(2, 2, 42, 42, image)