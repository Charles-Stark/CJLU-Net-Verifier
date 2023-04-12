"""
@Project : CJLU-Net-Verifier
@File    : app.py
@Author  : Charles Stark
@Date    : 2023/4/12 11:16
"""

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class InputDialog(QWidget):

    def __init__(self, parent=None):
        super(InputDialog, self).__init__(parent)
        layout = QFormLayout()

        self.btn1 = QPushButton("获得列表里的选项")
        self.btn1.clicked.connect(self.getItem)
        self.le1 = QLineEdit()
        layout.addRow(self.btn1, self.le1)

        self.btn2 = QPushButton("获得字符串")
        self.btn2.clicked.connect(self.getIext)
        self.le2 = QLineEdit()
        layout.addRow(self.btn2, self.le2)

        self.btn3 = QPushButton("获得整数")
        self.btn3.clicked.connect(self.getInt)
        self.le3 = QLineEdit()
        layout.addRow(self.btn3, self.le3)
        self.setLayout(layout)
        self.setWindowTitle("Input Dialog 示例")

    def getItem(self):
        items = ("C", "C++", "Java", "Python")
        item, ok = QInputDialog.getItem(self, "select input dialog",
                                        "语言列表", items, 0, False)
        if ok and item:
            self.le1.setText(item)

    def getIext(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', '输入姓名:')
        if ok:
            self.le2.setText(str(text))

    def getInt(self):
        num, ok = QInputDialog.getInt(self, "integer input dualog", "输入数字")
        if ok:
            self.le3.setText(str(num))


class Tray(QSystemTrayIcon):

    def __init__(self, _app):
        super().__init__()

        self.app = _app
        self.on_icon = QIcon('./asset/on.png')
        self.off_icon = QIcon('./asset/off.png')

        self.setIcon(self.off_icon)
        self.setVisible(True)

        self.menu = QMenu()

        self.action_input_info = QAction('添加账户')
        self.action_input_info.triggered.connect(self.input_info)
        self.menu.addAction(self.action_input_info)

        self.action_connect = QAction('手动连接')
        self.action_connect.triggered.connect(self.connect)
        self.menu.addAction(self.action_connect)

        self.action_stay_connected = QAction('自动连接')
        self.action_stay_connected.triggered.connect(self.stay_connected)
        self.menu.addAction(self.action_stay_connected)

        self.menu.addSeparator()

        self.action_auto_start = QAction('开机自启')
        self.action_auto_start.triggered.connect(self.auto_start)
        self.menu.addAction(self.action_auto_start)

        self.action_show_about = QAction('关于')
        self.action_show_about.triggered.connect(self.show_about)
        self.menu.addAction(self.action_show_about)

        self.action_quit = QAction('退出')
        self.action_quit.triggered.connect(self.quit_app)
        self.menu.addAction(self.action_quit)

        self.setContextMenu(self.menu)

    def input_info(self):
        window = InputDialog()
        window.show()

    def connect(self):
        pass

    def stay_connected(self):
        pass

    def auto_start(self):
        pass

    def show_about(self):
        dialog = QDialog(self.menu)
        dialog.setWindowTitle('关于')
        dialog.exec()

    def quit_app(self):
        self.app.quit()


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    tray = Tray(app)

    app.exec()
