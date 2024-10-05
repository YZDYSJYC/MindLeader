# coding=utf-8
# 作者: 拓跋龙
# 功能: 音乐界面

from qfluentwidgets import PushButton
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from gui.music.buttons import PlayButton
from source.client.music.music import MusicPlayer

class MusicPage(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setObjectName('music_page')

        self.add_top_widgets()
        self.add_mid_widgets()
        self.add_bottom_widgets()
        self.player = MusicPlayer(50)

    def add_top_widgets(self):
        self.top_widget = QWidget()

    def add_mid_widgets(self):
        self.mid_widget = QWidget()

    def add_bottom_widgets(self):
        self.bottom_widget = QWidget()

        bottom_layout = QHBoxLayout(self.bottom_widget)
        self.last_song_btn = PushButton()
        self.play_btn = PlayButton()
        self.play_btn.clicked.connect(lambda: self.play())
        bottom_layout.addWidget(self.play_btn)

        self._layout.addWidget(self.bottom_widget)

    def play(self):
        is_playing = self.play_btn.isPlaying
        self.play_btn.setPlay(is_playing)
        if is_playing:
            self.player.play()
        else:
            self.player.pause()