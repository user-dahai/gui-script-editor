# -*-coding:utf-8-*-
"""
pyw格式：运行时不显示黑窗
打包命令：pyinstaller -F app.pyw -i favicon.ico
"""

from main import *


if __name__ == '__main__':
    # 实例化
    app = QApplication(sys.argv)
    start = Main()
    # 显示
    start.show()
    app.exit(app.exec_())