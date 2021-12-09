# -*-coding:utf-8-*-

"""
隐藏窗口运行时浮窗可以使用停止功能
"""

from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication


class FloatingWin(QWidget):
    def __init__(self, main_win=None):
        super(FloatingWin, self).__init__()
        self.main_win = main_win
        self._startPos = None
        self._wmGap = None
        self.hidden = False
        self.ui_alive = True
        self.cpu_gui_x = 75
        self.label_size = 'font: 13px'

        # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置透明度(0~1)
        self.setWindowOpacity(1)
        # 设置鼠标为手状
        self.setCursor(Qt.PointingHandCursor)

        self.window_width = 32
        self.window_height = 32
        self.resize(self.window_width, self.window_height)

        # 停止按钮
        self.stop_btn = QPushButton("||", self)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setStyleSheet("""color: red;
border-style:none;
border:1px solid red; 
height: 30px;
width: 30px;
border-radius:16px;
background-color: rgb(50, 50, 50);
""")
        self.stop_btn.setWindowOpacity(1)
        self.stop_btn.clicked.connect(self.stop)

        # 设置最初出现的位置
        dsk = QApplication.primaryScreen()
        self.screen_width = dsk.geometry().width()
        self.screen_height = dsk.geometry().height()
        window_width = self.geometry().width()
        window_height = self.geometry().height()
        self.setGeometry(self.screen_width - window_width, self.screen_height // 2 - 150, window_width, window_height)

        # 快捷键

    def enterEvent(self, event):
        self.hide_or_show('show', event)

    def leaveEvent(self, event):
        self.hide_or_show('hide', event)

    def hide_or_show(self, mode, event):
        # 获取窗口左上角x,y
        pos = self.frameGeometry().topLeft()
        if mode == 'show' and self.hidden:
            # 窗口左上角x + 窗口宽度 大于屏幕宽度，从右侧滑出
            if pos.x() + self.window_width >= self.screen_width:
                # 需要留10在里边，否则边界跳动
                self.start_animation(self.screen_width - self.window_width, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角x 小于0, 从左侧滑出
            elif pos.x() <= 0:
                self.start_animation(0, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角y 小于0, 从上方滑出
            elif pos.y() <= 0:
                self.start_animation(pos.x(), 0)
                event.accept()
                self.hidden = False
        elif mode == 'hide' and (not self.hidden):
            if pos.x() + self.window_width >= self.screen_width:
                # 留10在外面
                self.start_animation(self.screen_width - 10, pos.y(), mode, 'right')
                event.accept()
                self.hidden = True
            elif pos.x() <= 0:
                # 留10在外面
                self.start_animation(10 - self.window_width, pos.y(), mode, 'left')
                event.accept()
                self.hidden = True
            elif pos.y() <= 0:
                # 留10在外面
                self.start_animation(pos.x(), 10 - self.window_height, mode, 'up')
                event.accept()
                self.hidden = True

    def start_animation(self, x, y, mode='show', direction=None):
        animation = QPropertyAnimation(self, b"geometry", self)
        # 滑出动画时长
        animation.setDuration(200)
        # 隐藏时，只留10在外边，防止跨屏
        # QRect限制其大小，防止跨屏
        num = QApplication.desktop().screenCount()
        if mode == 'hide':
            if direction == 'right':
                animation.setEndValue(QRect(x, y, 10, self.window_height))
            elif direction == 'left':
                # 多屏时采用不同的隐藏方法，防止跨屏
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(0, y, 10, self.window_height))
            else:
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(x, 0, self.window_width, 10))
        else:
            animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
        animation.start()

    def stop(self):
        if self.main_win is not None:
            try:
                self.main_win.run_script("浮窗")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    # 实例化
    app = QApplication([])
    start = FloatingWin()

    # 显示
    start.show()
    app.exit(app.exec_())
