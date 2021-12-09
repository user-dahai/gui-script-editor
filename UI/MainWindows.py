# -*-coding:utf-8-*-
"""
主界面：
    1.继承布局，并在布局的基础上加入表格、按钮等元素
"""


from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QTextEdit, QLabel, QPushButton, QCheckBox, QLineEdit

from Setup.ProjectData import ProjectData
from UI.MainLayout import MainLayout
from UI.MainTable import MainTable


class MainWindows(MainLayout, ProjectData):
    def __init__(self):
        super(MainWindows, self).__init__()

        self.setWindowTitle("图像识别脚本工具")
        self.setWindowIcon(QIcon("favicon.ico"))
        self.resize(1000, 700)  # 设置尺寸

        # 输出台
        self.result_le = QTextEdit(self)
        self.result_le.setStyleSheet("color:white;background-color: black;font-size:16px")
        self.result_le.append('欢迎使用图像识别脚本工具~这里是运行日志')
        self.hly_output.addWidget(self.result_le)

        # 编辑器标题
        self.table_title = QLabel(self)
        self.table_title.setText('脚本编辑器                                              运行次数：')
        self.table_title.setContentsMargins(5, 5, 5, 5)
        self.hly_edit.addWidget(self.table_title)

        # 运行次数
        self.run_times_btn = QLineEdit()
        self.run_times_btn.setValidator(QIntValidator(1, 999999))
        self.run_times_btn.setText(self.retry)
        self.hly_edit.addWidget(self.run_times_btn)

        # 编辑器
        self.table = MainTable(self.CurrentProject["path"] + "/cmd.xls", self.column_name)
        self.vly_edit.addWidget(self.table)

        # 指令说明
        self.note = QLabel(self)
        self.note.setText('操作说明：\n\n'
                          '     指令类型：1 单击  2 双击  3 右键  4 输入  5 等待  6 滚轮\n'
                          '     内    容：图片名称.png、输入内容、等待时长/秒\n'
                          '     重复次数：-1代表一直重复\n'
                          '     截    屏：拖拽选择截屏区域，右键确认截屏（自动保存，并拷贝图片名称），ESC退出截屏')
        self.note.setContentsMargins(10, 10, 10, 10)
        self.vly_edit.addWidget(self.note)

        # 文件按钮
        self.create_btn = QPushButton('新建脚本', self)
        self.open_btn = QPushButton('打开脚本', self)
        self.save_btn = QPushButton('保存脚本', self)
        self.save_btn.setDisabled(True)
        for i in (self.create_btn, self.open_btn, self.save_btn):
            self.hly_file_button.addWidget(i)

        # 运行或截屏时隐藏窗口
        self.hide_while_run_btn = QCheckBox("运行或截屏隐藏窗口")
        self.hide_while_run_btn.setChecked(bool(int(self.hide_while_run)))
        self.hly_file_button.addWidget(self.hide_while_run_btn)

        # 按钮
        self.add_rows_btn = QPushButton('插入一行', self)
        self.del_rows_btn = QPushButton('删除一行', self)
        self.screenshot_btn = QPushButton('截屏', self)
        self.run_btn = QPushButton('运行脚本', self)
        for i in (self.add_rows_btn, self.del_rows_btn, self.screenshot_btn, self.run_btn):
            self.hly_button.addWidget(i)

