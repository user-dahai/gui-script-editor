# -*-coding:utf-8-*-
"""
布局
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel


class MainLayout(QWidget):

    def __init__(self):
        super(MainLayout, self).__init__()

        self.hly_body = QHBoxLayout(self)
        self.hly_body.setContentsMargins(0, 0, 0, 0)
        self.hly_body.setSpacing(0)
        self.hly_body.setObjectName("hly_body")

        # 编辑器区
        self.vly_edit = QVBoxLayout()
        self.hly_body.addLayout(self.vly_edit)
        # 工具栏标题
        self.button_title = QLabel(self)
        self.button_title.setText('工具栏')
        self.button_title.setContentsMargins(5, 5, 5, 5)
        self.vly_edit.addWidget(self.button_title)
        # 文件按钮栏
        self.hly_file_button = QHBoxLayout()
        self.vly_edit.addLayout(self.hly_file_button)
        # 操作按钮栏
        self.hly_button = QHBoxLayout()
        self.vly_edit.addLayout(self.hly_button)
        # 编辑器标题
        self.hly_edit = QHBoxLayout()
        self.vly_edit.addLayout(self.hly_edit)
        # 输出台
        self.widget_output = QWidget()
        self.hly_output = QHBoxLayout(self.widget_output)
        self.hly_output.setContentsMargins(0, 0, 0, 0)
        self.hly_output.setObjectName("hly_output")
        self.hly_body.addWidget(self.widget_output)

