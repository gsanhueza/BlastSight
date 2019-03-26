#!/usr/bin/env python

import sys
from PySide2.QtWidgets import QApplication

from View.mainwindow import MainWindow


if __name__ == "__main__":
    # Qt Application
    qt_app = QApplication(sys.argv)

    # MainWindow using QWidget as central widget
    window = MainWindow()

    window.show()
    sys.exit(qt_app.exec_())
