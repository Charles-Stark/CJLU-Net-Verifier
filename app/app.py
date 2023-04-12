"""
@Project : CJLU-Net-Verifier
@File    : app.py
@Author  : Charles Stark
@Date    : 2023/4/12 11:16
"""

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class InputWindow(QWidget):

    def __init__(self, parent=None):
        super(InputWindow, self).__init__(parent)

        layout = QFormLayout()

        self.label1 = QLabel()
        self.label1.setText('校园网')
        layout.addRow(self.label1)

        self.label2 = QLabel()
        self.label2.setText('用户名')
        self.lineEdit2 = QLineEdit()
        layout.addRow(self.label2, self.lineEdit2)

        self.label3 = QLabel()
        self.label3.setText('密码')
        self.lineEdit3 = QLineEdit()
        layout.addRow(self.label3, self.lineEdit3)

        self.label4 = QLabel()
        self.label4.setText('VPN')
        layout.addRow(self.label4)

        self.label5 = QLabel()
        self.label5.setText('用户名')
        self.lineEdit5 = QLineEdit()
        layout.addRow(self.label5, self.lineEdit5)

        self.label6 = QLabel()
        self.label6.setText('密码')
        self.lineEdit6 = QLineEdit()
        layout.addRow(self.label6, self.lineEdit6)

        self.setLayout(layout)
        self.setWindowTitle('添加账户')


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

        self.window = InputWindow()

    def input_info(self):
        self.window.show()

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
