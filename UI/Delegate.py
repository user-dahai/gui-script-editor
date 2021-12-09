# -*-coding:utf-8-*-
"""
用于表格输入内容的限制
"""


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QItemDelegate, QLineEdit


class DoubleOnlyDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(DoubleOnlyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        editor = QLineEdit(QWidget)
        editor.setValidator(QDoubleValidator())
        return editor

    def setEditorData(self, lineEdit, QModelIndex):
        text = QModelIndex.model().data(QModelIndex, Qt.EditRole)
        lineEdit.setText(str(text))

    def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
        QWidget.setGeometry(QStyleOptionViewItem.rect)

    def setModelData(self, lineEditor, QAbstractItemModel, QModelIndex):
        text = lineEditor.text()
        QAbstractItemModel.setData(QModelIndex, text, Qt.EditRole)


class IntOnlyDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(IntOnlyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        editor = QLineEdit(QWidget)
        editor.setValidator(QIntValidator())
        return editor

    def setEditorData(self, lineEdit, QModelIndex):
        text = QModelIndex.model().data(QModelIndex, Qt.EditRole)
        lineEdit.setText(str(text))

    def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
        QWidget.setGeometry(QStyleOptionViewItem.rect)

    def setModelData(self, lineEditor, QAbstractItemModel, QModelIndex):
        text = lineEditor.text()
        QAbstractItemModel.setData(QModelIndex, text, Qt.EditRole)