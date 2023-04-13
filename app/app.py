"""
@Project : CJLU-Net-Verifier
@File    : app.py
@Author  : Charles Stark
@Date    : 2023/4/12 11:16
"""
import configparser
import os.path
import sys

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from net.verify import *


class InputWindow(QWidget):

    def __init__(self, conf_path, parent=None):
        super(InputWindow, self).__init__(parent)

        layout = QFormLayout()

        font = self.font()
        font.setBold(True)
        font.setPointSize(10)

        self.label1 = QLabel('校园网')
        self.label1.setFont(font)
        layout.addRow(self.label1)

        self.label2 = QLabel('用户名')
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedSize(290, 25)
        layout.addRow(self.label2, self.lineEdit2)

        self.label3 = QLabel('密码')
        self.lineEdit3 = QLineEdit()
        self.lineEdit3.setEchoMode(QLineEdit.echoMode(self.lineEdit3).Password)
        self.lineEdit3.setFixedSize(290, 25)
        layout.addRow(self.label3, self.lineEdit3)

        self.label4 = QLabel('VPN')
        self.label4.setFont(font)
        layout.addRow(self.label4)

        self.label5 = QLabel('用户名')
        self.lineEdit5 = QLineEdit()
        self.lineEdit5.setFixedSize(290, 25)
        layout.addRow(self.label5, self.lineEdit5)

        self.label6 = QLabel('密码')
        self.lineEdit6 = QLineEdit()
        self.lineEdit6.setEchoMode(QLineEdit.echoMode(self.lineEdit6).Password)
        self.lineEdit6.setFixedSize(290, 25)
        layout.addRow(self.label6, self.lineEdit6)

        self.button = QPushButton('确定')
        self.button.setFixedHeight(32)
        self.button.released.connect(self.save_info)
        layout.addRow(self.button)

        self.setLayout(layout)
        self.setWindowTitle('添加账户')
        self.setFixedSize(360, 222)

        self.conf_path = conf_path

    def save_info(self):
        if self.lineEdit2.text().strip() == '' or self.lineEdit3.text().strip() == '' or \
                self.lineEdit5.text().strip() == '' or self.lineEdit6.text().strip() == '':
            QMessageBox.critical(QWidget(), '输入错误', '输入不能为空')
            return

        conf = configparser.ConfigParser()

        conf.add_section('net')
        conf.set('net', 'username', self.lineEdit2.text())
        conf.set('net', 'password', self.lineEdit3.text())
        conf.add_section('vpn')
        conf.set('vpn', 'username', self.lineEdit5.text())
        conf.set('vpn', 'password', self.lineEdit6.text())
        conf.write(open(self.conf_path, 'w'))

        self.close()


class Tray(QSystemTrayIcon):

    def __init__(self, _app):
        super().__init__()

        self.app = _app
        self.on_icon = QIcon('./asset/on.png')
        self.off_icon = QIcon('./asset/off.png')
        self.tick_icon = QIcon('./asset/tick.png')

        self.is_connected = False

        self.setIcon(self.off_icon)
        self.setVisible(True)

        self.menu = QMenu()

        self.action_input_info = QAction('添加账户')
        self.action_input_info.triggered.connect(self.input_info)
        self.menu.addAction(self.action_input_info)

        self.action_connect = QAction('手动连接')
        self.action_connect.setIcon(self.tick_icon)
        self.action_connect.setIconVisibleInMenu(self.is_connected)
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

        self.conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
        self.window = InputWindow(self.conf_path)

    def input_info(self):
        self.window.show()

    def connect(self):
        if self.is_connected:
            # 断开连接
            if ping():
                # 有网
                vpn_disconnect('l2tp')

            self.action_connect.setIconVisibleInMenu(False)
            self.action_connect.setText('手动连接')
            self.is_connected = False
        else:
            # 手动连接
            if not ping():
                # 没网
                conf = configparser.ConfigParser()
                conf.read(self.conf_path, encoding='utf-8')

                if not net_verify(conf['net']['username'], conf['net']['password']):
                    QMessageBox.critical(QWidget(), '连接失败', '请检查校园网用户名和密码并重试')
                    return
                elif not vpn_verify('l2tp', conf['vpn']['username'], conf['vpn']['password']):
                    QMessageBox.critical(QWidget(), '连接失败', '请检查VPN设置并重试')
                    return

            self.action_connect.setIconVisibleInMenu(True)
            self.action_connect.setText('断开连接')
            self.is_connected = True

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

    sys.exit(app.exec())
