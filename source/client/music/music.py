# coding=utf-8
# 作者: 拓跋龙
# 功能: 音乐功能

import os

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

# 播放模式
RANDOM_MODE = 0
SEQUENTIAL_MODE = 1
CIRCULATE_MODE = 2
CIRCULATE_ONCE_MODE = 3

class MuiscBaseInfo:
    def __init__(self, name: str, auther: str, music_path: str, lyric: str):
        self.name = name
        self.auther = auther
        self.music_path = music_path
        self.lyric = lyric

class MusicPlayer:
    def __init__(self, volume: float) -> None:
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput() # 不能实例化为临时变量，否则被自动回收导致无法播放
        self.player.setAudioOutput(self.audio_output)
        # Pyside6中`QMediaPlayer.setVolume`已被移除，使用`QAudioOutput.setVolume`替代
        self.audio_output.setVolume(volume)
        self.play_mode = RANDOM_MODE
        self.set_cur_playing()

    def set_cur_playing(self):
        self.player.setSource(QUrl.fromLocalFile(os.path.join(os.getcwd(), 'config/music/dydjs.wav')))

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def set_play_mode(self, play_mode: int):
        if play_mode < 0 or play_mode > 3:
            print('输入的播放模式异常! 模式: ', play_mode)
            return
        self.play_mode = play_mode