"""
@Project : CJLU-Net-Verifier
@File    : app.py
@Author  : Charles Stark
@Date    : 2023/4/12 11:16
"""

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Tray(QSystemTrayIcon):

    def __init__(self, *__args):
        super().__init__(*__args)

        self.on_icon = QIcon('')
        self.off_icon = QIcon('')
        self.setIcon(self.off_icon)
        self.setVisible(True)

        # tray.setContextMenu(menu)


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    tray = Tray()

    app.exec()
