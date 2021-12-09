# -*-coding:utf-8-*-
"""
主程序
    1：继承主界面、为界面上面的按钮的绑定各自的功能
    2：实例运行线程，关联线程信号
    3：实例浮窗
"""


import os
import sys

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication

from Action import ScreenShot
from ScriptThread.RunnerThread import *
from UI.FloatingWin import FloatingWin
from UI.MainWindows import MainWindows


class Main(MainWindows):
    runner_control = pyqtSignal(list)

    def __init__(self):
        super(Main, self).__init__()
        # 绑定点击事件：新建脚本，打开脚本，保存脚本
        self.create_btn.clicked.connect(self.create_project)
        self.open_btn.clicked.connect(self.open_project)
        self.save_btn.clicked.connect(self.save_project)

        # 绑定点击事件：增加一行，截屏，运行脚本
        self.add_rows_btn.clicked.connect(lambda: self.edit_row("add"))
        self.del_rows_btn.clicked.connect(lambda: self.edit_row("del"))
        self.screenshot_btn.clicked.connect(self.screen_shot)
        self.run_btn.clicked.connect(self.run_script)

        # 绑定修改事件：表格
        self.table.cellChanged.connect(self.cell_change)

        # 运行线程
        self.runner = RunnerThread(self.CurrentProject["path"] + "/cmd.xls")
        self.runner.signal.connect(self.callback)
        self.runner_control.connect(self.runner.params_update)
        self.runner_status = False

        # 浮窗
        self.float_btn = FloatingWin(self)

    def create_project(self):
        """
        新建脚本
        """
        path, filetype = QFileDialog.getSaveFileName(self, "新建脚本", self.CurrentProject["dir"], "Directory")
        self.callback(path)
        if path:
            os.makedirs(path, exist_ok=True)
            self.CurrentProject["path"] = path
            self.CurrentProject["status"] = "new"
            self.update_project_att("path")
            self.table.setRowCount(0)
            self.table.addRowColumn()

    def open_project(self):
        """
        打开脚本
        这个函数的第二个参数是对话框的标题，第三个参数是设置打开文件的目录。当然我们还可以增加第四个，也就是增加一个过滤器，以便仅显示与过滤器匹配的文件。 例如：
        filename = QFileDialog.getOpenFileNames(self, '学点编程吧:打开多个文件','./',"Text files (*.txt)")
        """
        try:
            value = QFileDialog.getExistingDirectory(self, '', self.CurrentProject["dir"])
            if value:
                self.CurrentProject["path"] = value
                self.update_project_att("path")
                self.table.read_script_file(self.CurrentProject["path"] + "/cmd.xls")
                self.table.settable_init_data(self.column_name)
                self.CurrentProject["status"] = "old"
                self.save_project_data()
                self.save_btn.setDisabled(True)
        except Exception as e:
            self.callback(e)

    def save_project(self):
        """
        保存脚本
        """
        try:
            self.table.save_script_file(self.CurrentProject["path"] + "/cmd.xls")
            self.CurrentProject["status"] = "saved"
            self.save_project_data()
            self.save_btn.setDisabled(True)
        except Exception as e:
            self.callback(e.__str__())

    def edit_row(self, opt="add"):
        """
        增加一行
        """
        if opt == "add":
            self.table.addRowColumn()
        else:
            self.table.removeRowColumn()

    def screen_shot(self):
        """
        截屏
        """
        if self.hide_while_run_btn.isChecked():
            self.setHidden(True)
        ScreenShot.main(self.CurrentProject["path"])
        self.setHidden(False)

    def run_script(self, msg):
        """
        运行脚本
        """
        print("msg:", msg)
        self.hide_while_run_btn_change()
        if self.table.changed is True:
            answer = QMessageBox.question(self, "脚本已修改", "是否保存", QMessageBox.Yes | QMessageBox.No)
            if answer == 16384:
                try:
                    self.save_project()
                except Exception as e:
                    print(e)
            else:
                pass

        try:
            if self.runner_status is False:
                # self.result_le.clear()
                self.runner_status = True
                self.run_btn.setText("停止运行")
                self.update_runner_params()
                if self.hide_while_run_btn.isChecked():
                    self.setHidden(True)
                    self.float_btn.show()
                self.runner.start()

            elif self.runner_status is True:
                # 发射信号让脚本停下来
                self.runner_status = False
                self.setHidden(False)
                self.run_btn.setText("运行脚本")
                self.update_runner_params()
        except Exception as e:
            print(e)

    def callback(self, msg):
        """
        信号回调
        """
        if "end" in msg:
            try:
                self.runner_status = False

                self.setHidden(False)
                if self.hide_while_run_btn.isChecked():
                    self.float_btn.close()
                self.run_btn.setText("运行脚本")

            except Exception as e:
                print(e)
        self.result_le.append(msg)

    def update_runner_params(self):  # 中止参数
        """
        信号发射
        """
        self.runner_control.emit(self.runner_params())

    def runner_params(self):
        """
        信号参数
        """
        key = int(self.retry or "1")
        return list([self.runner_status, self.CurrentProject["path"] + "/cmd.xls", key])

    def cell_change(self):
        """
        表格编辑变更
        """
        self.save_btn.setDisabled(False)

    def hide_while_run_btn_change(self):
        """
        运行或截屏隐藏窗口选项
        """
        if self.hide_while_run_btn.isChecked():
            self.hide_while_run = "1"
        else:
            self.hide_while_run = "0"
        self.retry = self.run_times_btn.text()

        self.save_project_data()


if __name__ == '__main__':
    # 实例化
    app = QApplication(sys.argv)
    start = Main()
    # 显示
    start.show()
    app.exit(app.exec_())
