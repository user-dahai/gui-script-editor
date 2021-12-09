# -*-coding:utf-8-*-
"""
表格：用于编辑脚本，储存表格内容
"""
import os

import xlrd
import xlwt

from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem

from UI.Delegate import IntOnlyDelegate


# 基于Table Widget控件的表格
class MainTable(QTableWidget):
    def __init__(self, file, column_name=None, parent=None):
        super(MainTable, self).__init__(parent)

        # self.setShowGrid(False) #是否需要显示网格
        if column_name is None:
            column_name = ["a", "b", "c"]
        self.read_script_file(file)
        self.settable_init_data(column_name)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.addRowColumn()
        self.cellChanged.connect(self.cell_change)
        self.changed = False

    # ===1： 读取脚本文件
    def read_script_file(self, file):
        file_exit = os.path.exists(file)
        if file_exit is False:
            xls = xlwt.Workbook()
            sheet = xls.add_sheet("sheet1")
            xls.save(file)
        # 打开文件
        wb = xlrd.open_workbook(filename=file)
        # 通过索引获取表格sheet页
        self.sheet = wb.sheet_by_index(0)

    # ===2： 保存脚本文件
    def save_script_file(self, file):
        xls = xlwt.Workbook()
        sheet = xls.add_sheet("sheet1")

        # 表头
        sheet.write(0, 0, self.horizontalHeaderItem(0).text())
        sheet.write(0, 1, self.horizontalHeaderItem(1).text())
        sheet.write(0, 2, self.horizontalHeaderItem(2).text())

        for i in range(0, self.rowCount()):
            # 第一列
            if self.item(i, 0).text():
                text = float("%.1f" % float(self.item(i, 0).text()))
                sheet.write(i + 1, 0, text)
            else:
                sheet.write(i + 1, 0, self.item(i, 0).text())
            # 第二列
            sheet.write(i + 1, 1, self.item(i, 1).text())

            # 第三列
            if self.item(i, 2).text():
                sheet.write(i + 1, 2, float(self.item(i, 2).text()))
            else:
                sheet.write(i + 1, 2, self.item(i, 2).text())

        xls.save(file)
        self.changed = False

    # ===3:给表格输入初始化数据
    def settable_init_data(self, column_name):

        # ===1:创建初始表格
        self.setColumnCount(3)
        self.setRowCount(self.sheet.nrows - 1)

        # ===2:设置表格的表头名称
        self.setHorizontalHeaderLabels(column_name)
        self.changed = False

        # ===3:设置自定义委托限制输入整数
        try:
            self.setItemDelegateForColumn(0, IntOnlyDelegate())
        except Exception as e:
            print(e)

        for i in range(1, self.sheet.nrows):
            for j in range(3):

                # 2)直接在表格中添加数据
                self.setItem(i - 1, j, QTableWidgetItem(str(self.sheet.row(i)[j].value)))

    # ===4:数据变更
    def cell_change(self):
        self.changed = True

    # ===5:动态插入行列
    def addRowColumn(self):
        """当初始的行数或者列数不能满足需要的时候，
        我们需要动态的调整表格的大小，如入动态的插入行：
        insertColumn()动态插入列。
        insertRow(int)、
        insertColumn(int)，指定位置插入行或者列
        """
        row = self.rowCount() if self.currentRow() == -1 else self.currentRow()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(""))
        self.setItem(row, 1, QTableWidgetItem(""))
        self.setItem(row, 2, QTableWidgetItem(""))

    # ===6:动态移除行列
    def removeRowColumn(self):
        """
        removeColumn(int column) 移除column列及其内容。
        removeRow(int row)移除第row行及其内容。
        :return:
        """
        row = self.rowCount()-1 if self.currentRow() == -1 else self.currentRow()
        self.removeRow(row)


if __name__ == '__main__':
    # 实例化表格
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    myTable = MainTable("../../bad/cmd.xls")

    # 显示在屏幕中央
    # desktop = QApplication.desktop()  # 获取坐标
    # x = (desktop.width() - myTable.width()) // 2
    # y = (desktop.height() - myTable.height()) // 2
    # myTable.move(x, y)  # 移动

    # 显示表格
    myTable.show()
    app.exit(app.exec_())
