# -*-coding:utf-8-*-

"""
脚本运行线程
"""


from PyQt5.QtCore import QThread, pyqtSignal
from Action import ScriptRunner


class RunnerThread(QThread):
    signal = pyqtSignal(str)  # 括号里填写信号传递的参数

    def __init__(self, filename):
        super().__init__()
        self.runner = ScriptRunner.ScriptRunner()
        self.filename = filename
        self.pause = False
        self.key = "1"

    def run(self):
        # 线程启动
        try:
            self.runner.main(self.filename, self.signal, self.key)

        except Exception as e:
            self.signal.emit(e.__str__()) # 发射信号
        finally:
            self.signal.emit("=====================end=====================\n")  # 发射信号

    def params_update(self, params):  # 接受运行参数
        try:
            self.pause, self.filename, self.key = params
            self.runner.pause = self.pause
        except Exception as e:
            self.signal.emit(e.__str__())

    def set_file(self, filename):
        self.filename = filename
